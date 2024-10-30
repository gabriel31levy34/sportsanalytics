import pandas as pd
import matplotlib.pyplot as plt
from pybaseball import playerid_lookup, playerid_reverse_lookup
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime, timedelta
from shiny import App, render, ui
import io
import tempfile
from sqlalchemy import create_engine
import os

from pitcher_adv_report_helpers import classify_count, create_one_sheeter

### META INFORMATION
bottom_strike_zone = 1.52166
top_strike_zone = 3.67333
left_strike_zone = -0.83083
right_strike_zone = 0.83083

early = [(0,0), (1,0), (0,1), (1,1)]
ahead = [(2,0), (3,1), (3,0), (2,1)]
two_k = [(0,2), (1,2), (2,2), (3,2)]

target_cols = ['Pitch Type', 'Pitch%', 'Speed', 'Effective Speed', 'Spin', 'Extension', 'HB', 'VB', 'xwOBA']

start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
end_date = datetime.now().strftime("%Y-%m-%d")

# GET ALL DATA
username = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')
host = 'localhost'
database = 'statcast'

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{database}")

all_data = pd.read_sql(
    "SELECT * FROM statcast "
    "WHERE game_date BETWEEN '" + start_date + "' AND '" + end_date + "' "
    "AND pitch_type IS NOT NULL "
    "AND pitch_type != 'PO';",
    engine
)

engine.dispose()

all_data[['pfx_x', 'pfx_z']] = all_data[['pfx_x', 'pfx_z']] * 12
all_data['qual_count'] = all_data.apply(classify_count, axis=1)


def server(input, output, session):
    session.firstname = None
    session.lastname = None
    session.mlbam = None
    pdf_buffer = io.BytesIO()
    png_buffer = io.BytesIO()

    @output
    @render.text
    def report_status():
        if input.generate() == 0:
            return "Please enter a first name and last name, or MLBAM ID."
        
        # Handle empty first name and last name fields
        session.firstname = input.firstname().strip() if input.firstname().strip() else None
        session.lastname = input.lastname().strip() if input.lastname().strip() else None
        
        if input.mlbam().strip() == "":
            session.mlbam = None
            if session.firstname is not None and session.lastname is not None:
                try:
                    session.mlbam = playerid_lookup(session.lastname, session.firstname).key_mlbam.iloc[0]
                except IndexError:
                    return "Player not found. Please enter a valid first name and last name."
            else:
                return "You must enter a first name and last name, or MLBAM ID."
        else:
            try:
                session.mlbam = int(input.mlbam().strip())  # Attempt to convert to int
                player = playerid_reverse_lookup([session.mlbam], key_type='mlbam').iloc[0]
                session.firstname = player.name_first
                session.lastname = player.name_last
            except ValueError:
                session.mlbam = None

        # Generate status report
        if (session.firstname is None or session.lastname is None) and session.mlbam is None:
            return "Please enter a first name and last name, or MLBAM ID."
        
        return f"Generating report for {session.firstname.capitalize()} {session.lastname.capitalize()}..."

    @output
    @render.image
    def display_plot():
        # Ensure report is generated when the button is pressed
        if input.generate() == 0:
            return None

        # Generate and return the figure to be displayed in the plot output
        fig = create_one_sheeter(session.firstname, session.lastname, session.mlbam, input.batter_stand(), all_data)
        
        nonlocal pdf_buffer
        pdf_buffer = io.BytesIO()
        # png_buffer = io.BytesIO()
        
        with PdfPages(pdf_buffer) as pdf:
            pdf.savefig(fig, dpi=100, bbox_inches='tight')
            
        fig.savefig(png_buffer, format="png", dpi=100, bbox_inches='tight')
        plt.close(fig)
        
        # png_buffer.seek(0)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        png_path = temp_file.name

        fig.savefig(png_path, format="png", dpi=100, bbox_inches='tight')
        
        return {
            "src": png_path,
            "alt": "Pitcher Report",
            "width": "100%"
        }

    # Provide the PDF download functionality
    @session.download(filename="pitcher_adv_report.pdf")
    def download_report():
        if input.generate() == 0:
            return None
        
        nonlocal pdf_buffer

        # Move the buffer's cursor to the beginning so it can be read from the start
        pdf_buffer.seek(0)
        
        # Store the buffer for return
        buffer = pdf_buffer

        # Return the in-memory PDF buffer for download
        return buffer

    @output
    @render.ui
    def download_report_button():
        if input.generate() == 0:
            return None  # Only show download button after generating

        # Provide a download button (note: no href argument here)
        return ui.download_button("download_report", "Download PDF Report")


app_ui = ui.page_fluid(
    ui.h2("Baseball Statcast Pitcher Advance Report"),
    
    # Directly place the input fields in the UI
    ui.row(
        ui.column(3, ui.input_text("firstname", "First Name")),
        ui.column(3, ui.input_text("lastname", "Last Name")),
        ui.column(3, ui.input_text("mlbam", "MLBAM (Optional)")),
        ui.column(3, ui.input_radio_buttons("batter_stand", "Batter Stand", {"R": "Right", "L": "Left"}, selected="R")),
    ),
    
    # Add the action button and the download button in the same row
    ui.row(
        ui.column(3, ui.input_action_button("generate", "Generate Report")),
        ui.column(3, ui.output_ui("download_report_button"))
    ),
    
    ui.output_text_verbatim("report_status"),
    ui.output_plot("display_plot"),
)

    
app = App(app_ui, server)
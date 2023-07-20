<!-- PHP handler page that calls the aggregate stats sql script
  for pitchers based on user input -->

<html>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Amatic+SC&family=Sen&family=Stoke&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../css/styles.css">
<body>



  <div class="container-fluid">



  <?php
  $servername = "127.0.0.1"; // Do not use "localhost"

  // In the Real World (TM), you should not connect using the root account.
  // Create a privileged account instead.
  $username = "root";

  // In the Real World (TM), this password would be cracked in miliseconds.
  $password = "123456";

  // Create connection
  $conn = new mysqli($servername, $username, $password);

  // Check connection
  if ($conn->connect_error) {
      die("Connection failed: " . $conn->connect_error);
  }


  $dbname = "Baseball";

  mysqli_select_db($conn, $dbname) or die("Could not open the '$dbname'");

  $sDate = $_POST['sDate'];
  $eDate = $_POST['eDate'];
  $stat = $_POST['stat'];

    // Creating title and table headers
    echo "<div class='col align-self-center tables'>";
    echo "<h1> Aggregate statistics for pitchers by " . $stat ."</h1>";

    echo "<br>";
    echo "<div style='overflow-x:auto'>";
    echo "<table border='1'>";
    echo "<th>first_name</th>";
    echo "<th>last_name</th>";
    echo "<th>G</th>";
    echo "<th>IP</th>";
    echo "<th>AB</th>";
    echo "<th>PA</th>";
    echo "<th>H</th>";
    echo "<th>1B</th>";
    echo "<th>2B</th>";
    echo "<th>3B</th>";
    echo "<th>HR</th>";
    echo "<th>K</th>";
    echo "<th>BB</th>";
    echo "<th>K_percent</th>";
    echo "<th>BB_percent</th>";
    echo "<th>BAA</th>";
    echo "<th>SLG";
    echo "<th>OBP</th>";
    echo "<th>OPS</th>";
    echo "<th>ER</th>";
    echo "<th>R</th>";
    echo "<th>SV</th>";
    echo "<th>BS</th>";
    echo "<th>W</th>";
    echo "<th>L";
    echo "<th>ERA</th>";
    echo "<th>xBA</th>";
    echo "<th>xSLG</th>";
    echo "<th>wOBA</th>";
    echo "<th>xwOBA</th>";
    echo "<th>xISO</th>";
    echo "<th>Pitches</th>";
    echo "<th>four_seam_percent</th>";
    echo "<th>four_seam_avg_speed</th>";
    echo "<th>four_seam_avg_spin</th>";
    echo "<th>slider_percent</th>";
    echo "<th>slider_avg_speed</th>";
    echo "<th>slider_avg_spin</th>";
    echo "<th>change_up_percent</th>";
    echo "<th>change_up_avg_speed</th>";
    echo "<th>change_up_avg_spin</th>";
    echo "<th>curveball_percent</th>";
    echo "<th>curveball_avg_speed</th>";
    echo "<th>curveball_avg_spin</th>";
    echo "<th>sinker_percent</th>";
    echo "<th>sinker_avg_speed</th>";
    echo "<th>sinker_avg_spin</th>";
    echo "<th>cutter_percent</th>";
    echo "<th>cutter_avg_speed</th>";
    echo "<th>cutter_avg_spin</th>";
    echo "<th>splitter_percent</th>";
    echo "<th>splitter_avg_speed</th>";
    echo "<th>splitter_avg_spin</th>";
    echo "<th>knuckle_ball_percent</th>";
    echo "<th>knuckle_ball_avg_speed</th>";
    echo "<th>knuckle_ball_avg_spin</th>";


    // Call Sql Script using inputted variables
    $test_query = "CALL PitcherSeasonAggregate('$sDate', '$eDate', '$stat');";
    $result = mysqli_query($conn, $test_query);

    // for each row of sql data, add that to a table row
    while ($row = mysqli_fetch_array($result)) {
            echo "<tr>";
            for ($i=0; $i < 57; $i++) {
              echo "<td>" . $row[$i] . "</td>";
            }

            echo "</tr>";

    }
        echo "</table>";
        echo "</div>";
      echo "</div>";
    echo "</div>";

  ?>
</body>
</html>

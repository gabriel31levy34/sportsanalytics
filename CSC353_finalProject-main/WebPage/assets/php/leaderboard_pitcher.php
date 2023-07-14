<!-- PHP Handler page that creates a leaderboard of sorted pitchers by an
inputted statistic from the user -->


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

    // Create title and table with headers
    echo "<div class='col align-self-center tables'>";
    echo "<h1> Game Level Leaderboard for Pitching Statistics by SO</h1>";

    echo "<br>";
    echo "<div style='overflow-x:auto'>";
    echo "<table border='1'>";
    echo "<th>game_id</th>";
    echo "<th>player_id</th>";
    echo "<th>last_name</th>";
    echo "<th>first_name</th>";
    echo "<th>position</th>";
    echo "<th>bats</th>";
    echo "<th>throws</th>";
    echo "<th>height</th>";
    echo "<th>weight</th>";
    echo "<th>debut</th>";
    echo "<th>birthdate</th>";
    echo "<th>team</th>";
    echo "<th>days_rest</th>";
    echo "<th>IP</th>";
    echo "<th>H</th>";
    echo "<th>R</th>";
    echo "<th>ER</th>";
    echo "<th>BB</th>";
    echo "<th>SO</th>";
    echo "<th>HR</th>";
    echo "<th>HBP</th>";
    echo "<th>ERA</th>";
    echo "<th>BF</th>";
    echo "<th>pitches</th>";
    echo "<th>strikes_total</th>";
    echo "<th>strikes_looking </th>";
    echo "<th>strikes_swinging</th>";
    echo "<th>inplay_gb_total</th>";
    echo "<th>inplay_fb_total</th>";
    echo "<th>inplay_ld</th>";
    echo "<th>inplay_pu</th>";
    echo "<th>inplay_unk</th>";
    echo "<th>inherited_runners</th>";
    echo "<th>inherited_score</th>";
    echo "<th>SB</th>";
    echo "<th>CS</th>";
    echo "<th>pickoffs</th>";
    echo "<th>AB</th>";
    echo "<th>2B</th>";
    echo "<th>3B</th>";
    echo "<th>IBB</th>";
    echo "<th>GIDP</th>";
    echo "<th>SF</th>";
    echo "<th>ROE</th>";
    echo "<th>leverage_index_avg</th>";
    echo "<th>wpa_def</th>";
    echo "<th>cwpa_def</th>";
    echo "<th>re24_def</th>";
    echo "<th>date_game</th>";
    echo "<th>home_team</th>";
    echo "<th>away_team</th>";
    echo "<th>home_score</th>";
    echo "<th>away_score</th>";

    // Call SQL script using variables
    $test_query = "CALL pitcherGameLeaderboard('$sDate', '$eDate');";
    $result = mysqli_query($conn, $test_query);

    // For each role in SQL table add data to table row
    while ($row = mysqli_fetch_array($result)) {
            echo "<tr>";
            for ($i=0; $i < 53; $i++) {
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

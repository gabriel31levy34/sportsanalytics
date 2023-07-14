<!-- PHP handler page that gives takes in user input in order to either
aggregate pitcher game level statistics or give game level pitcher statistics for a
given player -->


<html>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Amatic+SC&family=Sen&family=Stoke&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../css/styles.css">
<body>
  <div class="container-fluid">
  <?php
    $servername = "127.0.0.1";
    $username = "root";
    $password = "123456";
    $conn = new mysqli($servername, $username, $password);
    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    $dbname = "Baseball";
    mysqli_select_db($conn, $dbname) or die("Could not open the '$dbname'");

    $pName = $_POST['pName'];
    // break name up to first and last
    $arr = explode(" ",$pName);
    $firstname = $arr[0];
    $lastname = $arr[1];
    $sDate = $_POST['sDate'];
    $eDate = $_POST['eDate'];
    $oName = $_POST['oName'];
    $local = $_POST['location'];
    $agg = $_POST['agg'];
    $stat = $_POST['stat'];

    // assign local to bit value based on input
    if ($local == 'Home'){
        $home = 1;
        $away = 0;
    }
    else {
        $home = 0;
        $away = 1;
    }

    // Checks if user wants aggregated data, which calls a different sql script
    if ($agg == 'Yes'){


      echo "<div class='col align-self-center tables'>";
      echo "<h1> Aggregate Pitcher Statistics at the Game Level</h1>";
      echo "<br>";
      echo "<div style='overflow-x:auto'>";
      echo "<table border='1'>";
      echo  "<th>first_name</th>";
      echo  "<th>last_name</th>";
      echo  "<th>G</th>";
      echo  "<th>IP</th>";
      echo  "<th>H</th>";
      echo  "<th>R</th>";
      echo  "<th>ER</th>";
      echo  "<th>BB</th>";
      echo  "<th>K</th>";
      echo  "<th>HR</th>";
      echo  "<th>HBP</th>";
      echo  "<th>BAA</th>";
      echo  "<th>ERA</th>";
      echo  "<th>BF</th>";
      echo "<th>pitches</th>";
      echo  "<th>strikes_total</th>";
      echo  "<th>ROE</th>";
      echo  "<th>GIDP</th>";
      echo  "<th>SB</th>";
      echo  "<th>CS</th>";
      echo  "<th>strikes_looking</th>";
      echo "<th>inplay_gb_total</th>";
      echo  "<th>inplay_ld</th>";
      echo  "<th>inplay_pu</th>";
      echo  "<th>inplay_unk</th>";
      echo  "<th>inherited_runners</th>";
      echo  "<th>inherited_score</th>";
      echo  "<th>SB</th>";
      echo  "<th>CS</th>";
      echo  "<th>pickoffs</th>";
      echo  "<th>AB</th>";
      echo  "<th>2B</th>";
      echo  "<th>3B</th>";
      echo  "<th>IBB</th>";
      echo  "<th>GIDP</th>";
      echo  "<th>SF</th>";
      echo  "<th>ROE</th>";
      echo  "<th>leverage_index_avg</th>";
      echo  "<th>wpa_def</th>";
      echo  "<th>cwpa_def</th>";
      echo  "<th>re24_def</th>";


      // Call Sql Script using inputted variables
        $test_query = "CALL PitcherGameAggregate('2015-10-10', '2021-01-01', 'G');";
        $result = mysqli_query($conn, $test_query);

        // for each row of sql data, add that to a table row
        while ($row = mysqli_fetch_array($result)) {
                echo "<tr>";
                for ($i=0; $i < 41; $i++) {
                    echo "<td>" . $row[$i] . "</td>";
                }
                echo "</tr>";
        }
            echo "</table>";
            echo "</div>";
            echo "</div>";
        echo "</div>";
      }

      // if not aggregate, run game stats for given player
    else{

      echo "<div class='col align-self-center tables'>";
      echo "<h1> Pitcher Game Statistics for " . $pName . "</h1>";
      echo "<br>";
      echo "<div style='overflow-x:auto'>";
      echo "<table border='1'>";
      echo  "<th>player_id</th>";
      echo  "<th>game_id</th>";
      echo  "<th>team</th>";
      echo  "<th>days_rest</th>";
      echo  "<th>IP</th>";
      echo  "<th>H</th>";
      echo  "<th>R</th>";
      echo  "<th>ER</th>";
      echo  "<th>BB</th>";
      echo  "<th>SO</th>";
      echo  "<th>HR</th>";
      echo  "<th>HBP</th>";
      echo  "<th>ERA</th>";
      echo  "<th>BF</th>";
      echo "<th>pitches</th>";
      echo  "<th>strikes_total</th>";
      echo  "<th>strikes_looking</th>";
      echo  "<th>strikes_swinging</th>";
      echo "<th>inplay_gb_total</th>";
      echo "<th>inplay_fb_total</th>";
      echo  "<th>inplay_ld</th>";
      echo  "<th>inplay_pu</th>";
      echo  "<th>inplay_unk</th>";
      echo  "<th>inherited_runners</th>";
      echo  "<th>inherited_score</th>";
      echo  "<th>SB</th>";
      echo  "<th>CS</th>";
      echo  "<th>pickoffs</th>";
      echo  "<th>AB</th>";
      echo  "<th>2B</th>";
      echo  "<th>3B</th>";
      echo  "<th>IBB</th>";
      echo  "<th>GIDP</th>";
      echo  "<th>SF</th>";
      echo  "<th>ROE</th>";
      echo  "<th>leverage_index_avg</th>";
      echo  "<th>wpa_def</th>";
      echo  "<th>cwpa_def</th>";
      echo  "<th>re24_def</th>";
      echo "<th>game_id</th>";
      echo "<th>date_game</th>";
      echo "<th>home_team</th>";
      echo "<th>away_team</th>";
      echo "<th>home_score</th>";
      echo "<th>away_score</th>";


      $test_query = "CALL pitcherGameStats('$firstname', '$lastname', '$oName', '$sDate', '$eDate', $home, $away);";
      $result = mysqli_query($conn, $test_query);
      $tuple_count = 0;
      while ($row = mysqli_fetch_array($result)) {
              echo "<tr>";
              for ($i=0; $i < 45; $i++) {
                  echo "<td>" . $row[$i] . "</td>";
              }
              echo "</tr>";
      }
          echo "</table>";
          echo "</div>";
          echo "</div>";
      echo "</div>";

    }









    ?>
    </body>
    </html>

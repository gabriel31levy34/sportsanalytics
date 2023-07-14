<!-- PHP page that calls php handler pages using forms to accumulate baseball data -->

<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Amatic+SC&family=Sen&family=Stoke&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="assets/css/styles.css">


    <title>Baseball Stats</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=default"></script>


</head>


  <body>

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

    ?>

<body>

    <div class="banner">
      <div class="content">
        <h1>Major League Baseball Statistics</h1>
        <div class="info">This site allows the user to make specific calls to players in order to
        access their game logs, statistics, or player info. </div>
        <h2>Game statistics for any game in a given year.</h2>
      </div>
    </div>


    <div class="container">
      <div class="row">
        <!-- Player Info Table -->
        <form action="assets/php/player.php" method="POST">
          <div class="d-flex justify-content-center">
              <label for="plName" class="top"><h2>Player Info</h2>
                <select name="plName" class="box">

                  <!-- Dropdown that calls the SQL in order to get all player names (as Full Name) -->
                  <option value="pName">--Select Player--</option>
                  <?php

                  $stmt4 = $conn->prepare("SELECT DISTINCT CONCAT(first_name, ' ', last_name) as name FROM Players ORDER BY name ASC;");

                  $stmt4->execute();
                  $result4 = $stmt4->get_result();
                  $used = array("");

                      while ($row = mysqli_fetch_array($result4)){
                        foreach ($row as $value) {
                          if (!in_array($value, $used)){
                            echo "<option value='$value'>$value</option>";
                            $used[] = $value;
                          }
                        }
                      }
                   ?>
                </select>
              </label>

          </div>
          <div class="d-flex justify-content-center">
            <input type="submit" class="col-3 top" value="Submit">
          </div>

        </form>

      </div>

      <div class="row">
        <form action="assets/php/team.php" method="POST">
          <div class="d-flex justify-content-center">
              <label for="tName" class="top"><h2> Team</h2>
                <select name="tName" class="box">
                  <!-- Dropdown that calls the SQL in order to get all team names in alpabetical order -->
                  <option>-- Select Team --</option>
                  <?php

                  $stmt4 = $conn->prepare("SELECT DISTINCT home_team FROM Game ORDER BY home_team ASC;");

                  $stmt4->execute();
                  $result4 = $stmt4->get_result();
                  $used = array("");

                      while ($row = mysqli_fetch_array($result4)){
                        foreach ($row as $value) {
                          if (!in_array($value, $used)){
                            echo "<option value='$value'>$value</option>";
                            $used[] = $value;
                          }
                        }
                      }
                   ?>
                </select>
              </label>
          </div>

          <div class="row">
            <div class="col-2"></div>

            <!-- Selector for Home or Away -->
            <div class="col-2">
              <label for="location" class="elem">
                <span class="align-top"><select name='location' class="box">
                  <option>-- Home/Away --</option>
                  <option> Home </option>
                  <option> Away</option>

                </select>
                </span>
                  </label>


            </div>

            <div class="col-2">
              <label for="oName" class="elem"></label>
                <span class="align-top"><select name='oName' class="box">

                  <!-- Dropdown that calls the SQL in order to get all team names for opponent -->
                  <option>-- Select Opponent --</option>
                  <option>ALL</option>
                  <?php

                  $stmt4 = $conn->prepare("SELECT DISTINCT away_team FROM Game ORDER BY away_team ASC;");

                  $stmt4->execute();
                  $result4 = $stmt4->get_result();
                  $used = array("");

                      while ($row = mysqli_fetch_array($result4)){
                        foreach ($row as $value) {
                          if (!in_array($value, $used)){
                            echo "<option value='$value'>$value</option>";
                            $used[] = $value;
                          }
                        }
                      }
                   ?>
                </select></span>
            </div>

            <!-- Calendar feature to select dates -->
            <div class="col-2">
              <label for="sDate" class="elem">Start Date</label>
                <span class="align-top">
                <input type="date" id="start" name="sDate" value = "2015-04-05" min="2015-04-05" max="2021-10-03"></span>
            </div>

            <div class="col-2">
              <label for="eDate" class="elem">End Date</label>
                <span class="align-top">
                <input type="date" id="end" name="eDate" value = "2015-04-05" min="2015-04-05" max="2021-10-03"></span>
            </div>

            <div class="d-flex justify-content-center">
              <input type="submit" class="col-3 top" value="Submit">
            </div>
          </div>
        </form>



      <div class="d-flex justify-content-center">
          <label for="pName" class="top"><h2> Pitchers</h2>
          </label>
      </div>
      <form action="assets/php/player_stats_pitcher.php" method="POST">
        <div class="row">
          <div class="col-3">
            <h2>Individual Pitcher Stats</h2>
          </div>

          <div class="col-4">
              <label for="pName" class="elem"></label>
                <span class="align-top"><select name='pName' class="box">

                  <!-- Dropdown that calls the SQL in order to get all player names (as Full Name) -->
                  <option>-- Select Pitcher --</option>
                  <?php

                  $stmt4 = $conn->prepare("SELECT DISTINCT CONCAT(first_name, ' ', last_name) as name FROM Players WHERE `position` LIKE 'pitcher' ORDER BY name ASC;");

                  $stmt4->execute();
                  $result4 = $stmt4->get_result();
                  $used = array("");

                      while ($row = mysqli_fetch_array($result4)){
                        foreach ($row as $value) {
                          if (!in_array($value, $used)){
                            echo "<option value='$value'>$value</option>";
                            $used[] = $value;
                          }
                        }
                      }
                  ?>
                </select></span>
            </div>

            <!-- All the years looked at in the CSV's  -->
          <div class="col-2">
            <label for="sDate" class="elem"></label>
              <select name='sDate' class="box">
                <option>-- Start Season --</option>
                <option>2015</option>
                <option>2016</option>
                <option>2017</option>
                <option>2018</option>
                <option>2019</option>
                <option>2020</option>
                <option>2021</option>
              </select>
          </div>
          <div class="col-2">
            <label for="eDate" class="elem"></label>
              <select name='eDate' class="box">
                <option>-- End Season --</option>
                <option>2015</option>
                <option>2016</option>
                <option>2017</option>
                <option>2018</option>
                <option>2019</option>
                <option>2020</option>
                <option>2021</option>
              </select>
          </div>
          <div class="col-2">

          </div>
          <div class="col-3"></div>
        </div>
        <div class="d-flex justify-content-center">
          <input type="submit" class="col-3 top" value="Submit">
        </div>
      </form>

      <form action="assets/php/aggregate_pitcher.php" method="POST">
        <div class="row">
          <div class="col-3">
            <h2>Pitcher Aggregate Stats</h2>
          </div>

          <div class="col-2">
            <label for="sDate" class="elem"></label>
              <select name='sDate' class="box">
                <option>-- Start Season --</option>
                <option>2015</option>
                <option>2016</option>
                <option>2017</option>
                <option>2018</option>
                <option>2019</option>
                <option>2020</option>
                <option>2021</option>
              </select>
          </div>
          <div class="col-2">
            <label for="eDate" class="elem"></label>
              <select name='eDate' class="box">
                <option>-- End Season --</option>
                <option>2015</option>
                <option>2016</option>
                <option>2017</option>
                <option>2018</option>
                <option>2019</option>
                <option>2020</option>
                <option>2021</option>
              </select>
          </div>

          <div class="col-2">
            <label for="stat" class="elem">Select Stat</label>
            <!-- Dropdown that calls the SQL in order to get all column names for pitcher stats -->
              <select name='stat' class="box">
                <option>-- Select Stat --</option>
                <?php
                $stmt4 = $conn->prepare("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='Baseball' AND TABLE_NAME='pitcherseasonstats' AND COLUMN_NAME != 'player_id' AND COLUMN_NAME != 'season' AND COLUMN_NAME != 'W' AND COLUMN_NAME != 'L' ;");

                $stmt4->execute();
                $result4 = $stmt4->get_result();
                $used = array("");

                    while ($row = mysqli_fetch_array($result4)){
                      foreach ($row as $value) {
                        if (!in_array($value, $used)){
                          echo "<option value='$value'>$value</option>";
                          $used[] = $value;
                        }
                      }
                    }
                 ?>
              </select>
          </div>

          <div class="col-3"></div>
        </div>


        <div class="d-flex justify-content-center">
          <input type="submit" class="col-3 top" value="Submit">
        </div>

      </form>


      <div class="d-flex justify-content-center">
          <label for="pName" class="top"><h2> Batter</h2>
          </label>
      </div>
      <form action="assets/php/player_stats_batter.php" method="POST">
        <div class="row">
          <div class="col-3">
            <h2>Individual Batter Stats</h2>
          </div>

        <div class="col-2">
            <label for="pName" class="elem"></label>
              <span class="align-top"><select name='pName' class="box">

                <!-- Dropdown that calls the SQL in order to get all player names (as Full Name) -->
                <option>-- Select Batter --</option>
                <?php

                $stmt4 = $conn->prepare("SELECT DISTINCT CONCAT(first_name, ' ', last_name) as name FROM Players WHERE `position` NOT LIKE 'pitcher' ORDER BY name ASC;");

                $stmt4->execute();
                $result4 = $stmt4->get_result();
                $used = array("");

                    while ($row = mysqli_fetch_array($result4)){
                      foreach ($row as $value) {
                        if (!in_array($value, $used)){
                          echo "<option value='$value'>$value</option>";
                          $used[] = $value;
                        }
                      }
                    }
                ?>
              </select></span>
          </div>

          <div class="col-2">
            <label for="sDate" class="elem"></label>
              <select name='sDate' class="box">
                <option>-- Start Season --</option>
                <option>2015</option>
                <option>2016</option>
                <option>2017</option>
                <option>2018</option>
                <option>2019</option>
                <option>2020</option>
                <option>2021</option>
              </select>
          </div>
          <div class="col-2">
            <label for="eDate" class="elem"></label>
              <select name='eDate' class="box">
                <option>-- End Season --</option>
                <option>2015</option>
                <option>2016</option>
                <option>2017</option>
                <option>2018</option>
                <option>2019</option>
                <option>2020</option>
                <option>2021</option>
              </select>
          </div>
          <div class="col-2">

          </div>
          <div class="col-3"></div>
        </div>
        <div class="d-flex justify-content-center">
          <input type="submit" class="col-3 top" value="Submit">
        </div>
      </form>

      <form action="assets/php/aggregate_batter.php" method="POST">
        <div class="row">
          <div class="col-3">
            <h2>Batter Aggregate Stats</h2>
          </div>

          <div class="col-2">
            <label for="sDate" class="elem"></label>
              <select name='sDate' class="box">
                <option>-- Start Season --</option>
                <option>2015</option>
                <option>2016</option>
                <option>2017</option>
                <option>2018</option>
                <option>2019</option>
                <option>2020</option>
                <option>2021</option>
              </select>
          </div>
          <div class="col-2">
            <label for="eDate" class="elem"></label>
              <select name='eDate' class="box">
                <option>-- End Season --</option>
                <option>2015</option>
                <option>2016</option>
                <option>2017</option>
                <option>2018</option>
                <option>2019</option>
                <option>2020</option>
                <option>2021</option>
              </select>
          </div>

          <!-- Selected aggregate stats for batter data  -->
          <div class="col-2">
            <label for="stat" class="elem">Select Stat</label>
              <select name='stat' class="box">
                <option>-- Select Stat --</option>
                <option><th>G</th></option>
                <option><th>AB</th></option>
                <option><th>PA</th></option>
                <option><th>H</th></option>
                <option><th>1B</th></option>
                <option><th>2B</th></option>
                <option><th>3B</th></option>
                <option><th>HR</th></option>
                <option><th>K</th></option>
                <option><th>BB</th></option>
                <option><th>K_percent</th></option>
                <option><th>BB_percent</th></option>
                <option><th>Average</th></option>
                <option><th>SLG </option>
                <option><th>OBP</th></option>
                <option><th>OPS</th></option>
                <option><th>RBI</th></option>
                <option><th>SB</th></option>
                <option><th>HBP</th></option>
                <option><th>R</th></option>
                <option><th>SB_percent</th></option>
                <option><th>xBA </option>
                <option><th>xSLG</th></option>
                <option><th>wOBA</th></option>
                <option><th>xwOBA</th></option>
                <option><th>xOBP</th></option>
                <th>xISO</th>
                <th>sprint_speed</th>;
              </select>
          </div>

          <div class="col-3"></div>
        </div>


        <div class="d-flex justify-content-center">
          <input type="submit" class="col-3 top" value="Submit">
        </div>

      </form>





      <div class="d-flex justify-content-center">
          <label for="stats" class="top"><h2> Game Level Statistics</h2>
          </label>
      </div>
      <form action="assets/php/batters.php" method="POST">

        <div class="row">
          <div class="col">
            <h2>Batters</h2>
          </div>

          <div class="col">
            <label for="pName" class="elem"></label>
            <span class="align-top"><select name='pName' class="box">

              <!-- Dropdown that calls the SQL in order to get all player names (as Full Name) -->
              <option>-- Select Batter --</option>
              <?php

              $stmt4 = $conn->prepare("SELECT DISTINCT CONCAT(first_name, ' ', last_name) as name FROM Players WHERE `position` NOT LIKE 'pitcher' ORDER BY name ASC;");

              $stmt4->execute();
              $result4 = $stmt4->get_result();
              $used = array("");

                  while ($row = mysqli_fetch_array($result4)){
                    foreach ($row as $value) {
                      if (!in_array($value, $used)){
                        echo "<option value='$value'>$value</option>";
                        $used[] = $value;
                      }
                    }
                  }
              ?>
            </select></span>
          </div>

          <div class="col">
              <label for="oName" class="elem"></label>
                <span class="align-top"><select name='oName' class="box">

                  <!-- Dropdown that calls the SQL in order to get team names as opponents -->
                  <option>-- Select Opponent --</option>
                  <option>ALL</option>
                  <?php

                  $stmt4 = $conn->prepare("SELECT DISTINCT away_team FROM Game ORDER BY away_team ASC;");

                  $stmt4->execute();
                  $result4 = $stmt4->get_result();
                  $used = array("");

                      while ($row = mysqli_fetch_array($result4)){
                        foreach ($row as $value) {
                          if (!in_array($value, $used)){
                            echo "<option value='$value'>$value</option>";
                            $used[] = $value;
                          }
                        }
                      }
                   ?>
                </select></span>
            </div>


            <div class="col">
              <label for="location" class="elem">
                <span class="align-top"><select name='location' class="box">
                  <option>-- Home/Away --</option>
                  <option value = "Home"> Home </option>
                  <option value = "Away"> Away</option>

                </select>
              </span>
              </label>
            </div>

          <div class="col">
            <label for="sDate" class="elem">Start Date</label>
              <span class="align-top">
              <input type="date" id="start" name="sDate" value = "2015-04-05" min="2015-04-05" max="2021-10-03"></span>
          </div>

          <div class="col">
            <label for="eDate" class="elem">End Date</label>
              <span class="align-top">
              <input type="date" id="end" name="eDate" value = "2015-04-05" min="2015-04-05" max="2021-10-03"></span>
          </div>

          <div class="col-2">
            <label for="stat" class="elem">Select Stat</label>
              <select name='stat' class="box">

                <!-- Dropdown that calls the SQL in order to get all column names for batter stats -->
                <option>-- Select Stat --</option>
                <?php
                $stmt4 = $conn->prepare("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='Baseball' AND TABLE_NAME='batterseasonstats' AND COLUMN_NAME != 'player_id' AND COLUMN_NAME != 'season' ;");

                $stmt4->execute();
                $result4 = $stmt4->get_result();
                $used = array("");

                    while ($row = mysqli_fetch_array($result4)){
                      foreach ($row as $value) {
                        if (!in_array($value, $used)){
                          echo "<option value='$value'>$value</option>";
                          $used[] = $value;
                        }
                      }
                    }
                 ?>
              </select>
          </div>

          <div class="col">
            <label for="agg" class="elem">Aggregate?</label>
              <select name='agg' class="box">
                <option>Yes</option>
                <option>No</option>
              </select>
          </div>





        <div class="d-flex justify-content-center">
          <input type="submit" class="col-3 top" value="Submit">
        </div>

      </form>

      <form action="assets/php/leaderboard_batter.php" method="POST">
        <div class="row">
          <div class="col-3">
            <h2>Batter Leaderboard Stats</h2>
          </div>

          <div class="col">
            <label for="sDate" class="elem">Start Date</label>
              <span class="align-top">
              <input type="date" id="start" name="sDate" value = "2015-04-05" min="2015-04-05" max="2021-10-03"></span>
          </div>

          <div class="col">
            <label for="eDate" class="elem">End Date</label>
              <span class="align-top">
              <input type="date" id="end" name="eDate" value = "2015-04-05" min="2015-04-05" max="2021-10-03"></span>
          </div>

          <div class="col-2">
            <label for="stat" class="elem">Select Stat</label>
              <select name='stat' class="box">
                <!-- Dropdown that calls the SQL in order to get all column names for pitcher season stats -->
                <option>-- Select Stat --</option>
                <?php
                $stmt4 = $conn->prepare("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='Baseball' AND TABLE_NAME='batterseasonstats' AND COLUMN_NAME != 'player_id' AND COLUMN_NAME != 'season' ;");

                $stmt4->execute();
                $result4 = $stmt4->get_result();
                $used = array("");

                    while ($row = mysqli_fetch_array($result4)){
                      foreach ($row as $value) {
                        if (!in_array($value, $used)){
                          echo "<option value='$value'>$value</option>";
                          $used[] = $value;
                        }
                      }
                    }
                 ?>
              </select>
          </div>



          <div class="col-3"></div>
        </div>


        <div class="d-flex justify-content-center">
          <input type="submit" class="col-3 top" value="Submit">
        </div>

      </form>



      <form action="assets/php/pitchers.php" method="POST">
        <div class="row">
          <div class="col">
            <h2>Pitchers</h2>
          </div>

          <div class="col">
              <label for="pName" class="elem"></label>
                <span class="align-top"><select name='pName' class="box">

                  <!-- Dropdown that calls the SQL in order to get all player names (as Full Name) -->
                  <option>-- Select Pitcher --</option>
                  <?php

                  $stmt4 = $conn->prepare("SELECT DISTINCT CONCAT(first_name, ' ', last_name) as name FROM Players WHERE `position` LIKE 'pitcher' ORDER BY name ASC;");

                  $stmt4->execute();
                  $result4 = $stmt4->get_result();
                  $used = array("");

                      while ($row = mysqli_fetch_array($result4)){
                        foreach ($row as $value) {
                          if (!in_array($value, $used)){
                            echo "<option value='$value'>$value</option>";
                            $used[] = $value;
                          }
                        }
                      }
                  ?>
                </select></span>
            </div>

            <div class="col">
              <label for="oName" class="elem"></label>
                <span class="align-top"><select name='oName' class="box">

                  <!-- Dropdown that calls the SQL in order to get all team names as opponent -->
                  <option>-- Select Opponent --</option>
                  <option>ALL</option>
                  <?php

                  $stmt4 = $conn->prepare("SELECT DISTINCT away_team FROM Game ORDER BY away_team ASC;");

                  $stmt4->execute();
                  $result4 = $stmt4->get_result();
                  $used = array("");

                      while ($row = mysqli_fetch_array($result4)){
                        foreach ($row as $value) {
                          if (!in_array($value, $used)){
                            echo "<option value='$value'>$value</option>";
                            $used[] = $value;
                          }
                        }
                      }
                   ?>
                </select></span>
            </div>


            <div class="col">
              <label for="location" class="elem">
                <span class="align-top"><select name='location' class="box">
                  <option>-- Home/Away --</option>
                  <option> Home </option>
                  <option> Away</option>

                </select>
                </span>
                  </label>
            </div>

          <div class="col">
            <label for="sDate" class="elem">Start Date</label>
              <span class="align-top">
              <input type="date" id="start" name="sDate" value = "2015-04-05" min="2015-04-05" max="2021-10-03"></span>
          </div>

          <div class="col">
            <label for="eDate" class="elem">End Date</label>
              <span class="align-top">
              <input type="date" id="end" name="eDate" value = "2015-04-05" min="2015-04-05" max="2021-10-03"></span>
          </div>

          <div class="col-2">
            <label for="stat" class="elem">Select Stat</label>
              <select name='stat' class="box">
                <!-- Dropdown that calls the SQL in order to get all column names for pitcher season stats -->
                <option>-- Select Stat --</option>
                <?php
                $stmt4 = $conn->prepare("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='Baseball' AND TABLE_NAME='pitcherseasonstats' AND COLUMN_NAME != 'player_id' AND COLUMN_NAME != 'season' ;");

                $stmt4->execute();
                $result4 = $stmt4->get_result();
                $used = array("");

                    while ($row = mysqli_fetch_array($result4)){
                      foreach ($row as $value) {
                        if (!in_array($value, $used)){
                          echo "<option value='$value'>$value</option>";
                          $used[] = $value;
                        }
                      }
                    }
                 ?>
              </select>
          </div>

          <div class="col">
            <label for="agg" class="elem">Aggregate?</label>
              <select name='agg' class="box">
                <option>Yes</option>
                <option>No</option>
              </select>
          </div>

          <div class="d-flex justify-content-center">
          <input type="submit" class="col-3 top" value="Submit">
        </div>


      </form>

      <form action="assets/php/leaderboard_pitcher.php" method="POST">
        <div class="row">
          <div class="col-3">
            <h2>Pitcher Leaderboard Stats</h2>
          </div>

          <div class="col-2">
            <label for="sDate" class="elem">Start Date</label>
              <span class="align-top">
              <input type="date" id="start" name="sDate" value = "2015-04-05" min="2015-04-05" max="2021-10-03"></span>
          </div>

          <div class="col-2">
            <label for="eDate" class="elem">End Date</label>
              <span class="align-top">
              <input type="date" id="end" name="eDate" value = "2015-04-05" min="2015-04-05" max="2021-10-03"></span>
          </div>

          <div class="col-2">
            <label for="stat" class="elem">Select Stat</label>
              <select name='stat' class="box">
                <!-- Dropdown that calls the SQL in order to get all column names for pitcher seaosn stats -->
                <option>-- Select Stat --</option>
                <?php
                $stmt4 = $conn->prepare("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='Baseball' AND TABLE_NAME='pitcherseasonstats' AND COLUMN_NAME != 'player_id' AND COLUMN_NAME != 'season' ;");

                $stmt4->execute();
                $result4 = $stmt4->get_result();
                $used = array("");

                    while ($row = mysqli_fetch_array($result4)){
                      foreach ($row as $value) {
                        if (!in_array($value, $used)){
                          echo "<option value='$value'>$value</option>";
                          $used[] = $value;
                        }
                      }
                    }
                 ?>
              </select>
          </div>

          <div class="col-3"></div>
        </div>


        <div class="d-flex justify-content-center">
          <input type="submit" class="col-3 top" value="Submit">
        </div>

      </form>

      <!-- Table used as a key for abbreviated statistics throughout page -->
      <div class="footer">
        <table>
    <tr>
      <th>Statistic</th>
      <th>Description</th>
    </tr>
    <tr>
      <td>G</td>
      <td>Game</td>
    </tr>
    <tr>
      <td>IP</td>
      <td>Innings Pitched</td>
    </tr>
    <tr>
        <td>PA</td>
        <td>Plate Appearance</td>
    </tr>
    <tr>
        <td>AB</td>
        <td>At Bat</td>
    </tr>
    <tr>
        <td>H</td>
        <td>Hit</td>
    </tr>
    <tr>
        <td>1B</td>
        <td>Single</td>
    </tr>
    <tr>
        <td>2B</td>
        <td>Double</td>
    </tr>
    <tr>
        <td>3B</td>
        <td>Triple</td>
    </tr>
    <tr>
        <td>HR</td>
        <td>Home run</td>
    </tr>
    <tr>
        <td>K</td>
        <td>Strike out</td>
    </tr>
    <tr>
        <td>BB</td>
        <td>Base on balls</td>
    </tr>
    <tr>
        <td>K_percent</td>
        <td>Strike out percent</td>
    </tr>
    <tr>
        <td>BB_percent</td>
        <td>Strike out percent</td>
    </tr>
    <tr>
        <td>BAA</td>
        <td>Batting average against</td>
    </tr>
    <tr>
        <td>SLG</td>
        <td>Slugging average</td>
    </tr>
    <tr>
        <td>OBP</td>
        <td>On base percentage</td>
    </tr>
    <tr>
        <td>OPS</td>
        <td>On base plus slugging</td>
    </tr>
    <tr>
        <td>ER</td>
        <td>Earned runs</td>
    </tr>
    <tr>
        <td>R</td>
        <td>Runs</td>
    </tr>
    <tr>
        <td>SV</td>
        <td>Saves</td>
    </tr>
    <tr>
        <td>BS</td>
        <td>Blown Saves</td>
    </tr>
    <tr>
        <td>W</td>
        <td>Wins</td>
    </tr>
    <tr>
        <td>L</td>
        <td>Losses</td>
    </tr>
    <tr>
        <td>ERA</td>
        <td>Earned run average</td>
    </tr>
    <tr>
        <td>xBA</td>
        <td>Expected batting average</td>
    </tr>
    <tr>
        <td>xSLG</td>
        <td>Expected slugging percentage</td>
    </tr>
    <tr>
        <td>wOBA</td>
        <td>Waited on base average</td>
    </tr>
    <tr>
        <td>xwOBA</td>
        <td>Expected waited on base average</td>
    </tr>
    <tr>
        <td>xOBP</td>
        <td>Expected on base percentage</td>
    </tr>
    <tr>
        <td>xISO</td>
        <td>Expected isolated power</td>
    </tr>
    <tr>
        <td>RBI</td>
        <td>Runs batted in</td>
    </tr>
    <tr>
        <td>HBP</td>
        <td>Hit by Pitch</td>
    </tr>
  </table>

      </div>

    </div>


    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>


</body>
</html>

<!-- PHP handler page that calls the aggregate stats sql script
  for batters based on user input -->

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
    echo "<h1> Leaderboard for top 100 batters ordered by " . $stat ."</h1>";

    echo "<br>";
    echo "<div style='overflow-x:auto'>";
    echo "<table border='1'>";
    echo "<th>first_name</th>";
    echo "<th>last_name</th>";
    echo "<th>G</th>";
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
    echo "<th>Average</th>";
    echo "<th>SLG";
    echo "<th>OBP</th>";
    echo "<th>OPS</th>";
    echo "<th>RBI</th>";
    echo "<th>SB</th>";
    echo "<th>HBP</th>";
    echo "<th>R</th>";
    echo "<th>SB_percent</th>";
    echo "<th>xBA";
    echo "<th>xSLG</th>";
    echo "<th>wOBA</th>";
    echo "<th>xwOBA</th>";
    echo "<th>xOBP</th>";
    echo "<th>xISO</th>";
    echo "<th>sprint_speed</th>";

    // Call Sql Script using inputted variables

    $test_query = "CALL BatterSeasonAggregate('$sDate', '$eDate', '$stat');";
    $result = mysqli_query($conn, $test_query);

    // for each row of sql data, add that to a table row
    while ($row = mysqli_fetch_array($result)) {
            echo "<tr>";
            for ($i=0; $i < 30; $i++) {
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

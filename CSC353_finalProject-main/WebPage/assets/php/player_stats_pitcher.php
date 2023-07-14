<!-- Gives overall season stats for user-inputted season years
for a given pitcher name -->


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

  $pName = $_POST['pName'];
  // split name into first and last names
  $arr = explode(" ",$pName);
  $firstname = $arr[0];
  $lastname = $arr[1];
  $sDate = $_POST['sDate'];
  $eDate = $_POST['eDate'];


  // Access sql schema to get column names to populate headers
  $test_query1 = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='Baseball' AND TABLE_NAME='pitcherseasonstats';";
  $result1 = mysqli_query($conn, $test_query1);

  echo "<div class='col align-self-center tables'>";
  echo "<h1> Pitcher Statistics for " . $pName . "</h1>";

  echo "<br>";
  echo "<div style='overflow-x:auto'>";
  echo "<table border='1' id=tb>";
  $counter = 0;
  // populate headers
  while ($row = mysqli_fetch_array($result1)) {
        echo "<th onclick='sortTable($counter)'>" . $row[0] . "</th>";
        $counter = $counter + 1;
      }

  // Call Sql Script using inputted variables
  $test_query = "CALL pitcherSeasonStats( '$sDate', $eDate, '$firstname', '$lastname');";
  $result = mysqli_query($conn, $test_query);

  // for each row of sql data, add that to a table row
  while ($row = mysqli_fetch_array($result)) {
          echo "<tr>";
          for ($i=0; $i < 61; $i++) {
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

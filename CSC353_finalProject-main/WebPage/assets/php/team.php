<!-- PHP Handler Page that returns team level statistics
for two teams matchups against each other based on a
date range and home/away information  -->


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

  $tname = $_POST['tName'];
  $local = $_POST['location'];
  $oname = $_POST['oName'];
  $sdate = $_POST['sDate'];
  $edate = $_POST['eDate'];

  // Assign local to bit value based on user input
  if ($local == 'Home'){
    $home = 1;
    $away = 0;
  }

  else {
    $home = 0;
    $away = 1;
  }



// Team season data based on dates and opponents
  $test_query = "CALL teamTable('$tname', '$oname', $home, $away, '$sdate', '$edate');";
  $result = mysqli_query($conn, $test_query);

  echo "<div class='col align-self-center tables'>";
  echo "<h1> Aggregate Statistics for " . $tname . " against " . $oname ."</h1>";

  echo "<br>";
  echo "<table border='1'>
          <tr>
          <th>Games_Played</th>
          <th>Win_PCT</th>
          <th>RF</th>
          <th>RA</th>";

  // for each row of sql data, add that to a table row
  while ($row = mysqli_fetch_array($result)) {


      echo "<tr>";
        echo "<td>" . $row[0]. "</td>";
        echo "<td>" . $row[1]. "</td>";
        echo "<td>" . $row[2]. "</td>";
        echo "<td>" . $row[3]. "</td>";

      echo "</tr>";
  }
      echo "</table>";
    echo "</div>";
  echo "</div>";
  ?>
</body>
</html>

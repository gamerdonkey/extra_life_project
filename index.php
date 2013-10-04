<html>
   <head>
   <title>
      Zach's Extra Life Extra Challenge
   </title>
      <script type="text/javascript" src="https://www.google.com/jsapi"></script>
      <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
      var data = google.visualization.arrayToDataTable([
<?php
   $extraLifeDb = new SQLite3('/home/gamerdonkey/extra_life_project/extra_life.db');
   $results = $extraLifeDb->query('select * from tallied_votes order by amount desc');

   $title_array = array("Title");
   $total_amount_array = array("Total");
   $vote_amount_array= array("Game Votes");
   $total = 0;
   $vote_total = 0;

   while($row = $results->fetchArray()){
      if($row[0] == "total") {
         $hours = $row[2]/100;
         $total = $row[2];
         $total_amount_array[] = $hours;
         $title_array[] = "Total";
         $vote_amount_array[] = 0;
      }
      elseif($row[0] == "voteTotal") {
         $vote_total = $row[2];
      }
      else {
         $total_amount_array[] = 0;
         $title_array[] = $row[1];
         $vote_amount_array[] = ($row[2]/$vote_total)*$total/100;
      }
   }
   echo json_encode($title_array).",";
   echo json_encode($total_amount_array).",";
   echo json_encode($vote_amount_array);
?>
        ]);

        var options = {
            'isStacked': true,
            hAxis: { title: 'Hours to Play' },
            height: 250,
            legend: { position: 'bottom' }
        };

        var chart = new google.visualization.BarChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
   </script>
   </head>
   <body>
      <div id="container" style="width: 1000px; margin: 0 auto;">
         <div class="page-title" style="width: 100%; text-align: center; font-size: 24pt;">
            <p sytle="">
               Zach's Extra Life Extra Challenge
            </p>
         </div>
         <div id="chart_div" style="width: 100%; height: 250px;"></div>
      </div>
   </body>
</html>


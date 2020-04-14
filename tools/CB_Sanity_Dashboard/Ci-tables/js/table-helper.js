
function getSanity() {
  
  $.ajax({
    dataType: "json",
    //url: "http://10.84.5.100/cs-shared/images/soumilk/final_result.json",
    url: "http://sanity-dashboard.englab.juniper.net/sanity/final_result.json",
    success: function(result) {
        //console.log(result);
        populateTable(result);
   },
    error: function() {
        console.log("Error in fecthing the ci data");
    }
  });
}

function asignClass(buildInfo) {
  if (buildInfo["Success rate"] == "100%") {
      return "green";
  } else {
      return "red";
  } 
}

function makeSanityElement(data) {
    if (data["isCompleted"]) {
        return "<a href=" + data["Report"] + ">" + 
          "<div>Sanity: " + data["Success rate"] + "(" + testsPassed + "/" + data["Total tests"] + ")" +
          "</a>"
    }
    else {
        return "";
    }
}

// construct table data cell for build information of ci information
function makeBuildTdBuilds(data) {
  var badgeClass = asignClass(data);
  //var testsPassed = parseInt(data["Total tests"]) - parseInt(data["Failures"]) - parseInt(data["Skipped"]) - parseInt(data["Errors"]);
  var testsPassed = parseInt(data["Total tests"]) - parseInt(data["Failures"]) - parseInt(data["Errors"]);
  return "<div class=" + badgeClass + ">" +

          "<a class='buildLink' href=" + data["BuildLink"] + ">Build ID: " + data["Build number"]+ "</a>" +
          
          "<a class='buildLink' href=" + data["Report"] + ">" + 
          "<div class='sanity'>Sanity: " + data["Success rate"] + " (" + testsPassed + "/" + data["Total tests"] + ") " +
          "</a>" +

          "<div class='ci-build-date'>" + data["Build date"] + "</div>" +

          "</div>";

}

// construct table data cell for build information of ci information (1st column)
function makeBuildTdJob(data) {
  return "<div>" + data["JobName"] + "</div>" +

          "<a href=" + data["lastGoddBuildLink"] + ">" + 
          "<div>Last good build: " + data["Last good build"] + "</div>" +
          "</a>" +
          
          "<a href=" + data["lastGoddBuildSanityLink"] + ">" + 
          "<div>Last good sanity: " + data["Last good sanity"] + "</div>" +
          "</a>"

}

function populateTable(sanity) {
  sanity = sanity["Sanity"];

  var jobs = sanity["Job"];

  // construct the ci information table
  $('#ci-info-table').DataTable({
    "data": jobs,
    columns : [
      {
        render: function (data, type, full, meta) {
          return makeBuildTdJob(full);
        }
      },
      {
        data: "Builds.0",
        render: function (data, type, full, meta) {
          return makeBuildTdBuilds(data);
        }
      },
      {
        data: "Builds.1",
        render: function (data, type, full, meta) {
          return makeBuildTdBuilds(data);
        }
      },

      {
        data: "Builds.2",
        render: function (data, type, full, meta) {
          return makeBuildTdBuilds(data);
        }
      },

      {
        data: "Builds.3",
        render: function (data, type, full, meta) {
          return makeBuildTdBuilds(data);
        }
      },

      {
        data: "Builds.4",
        render: function (data, type, full, meta) {
          return makeBuildTdBuilds(data);
        }
      }
    ]
  });


  var bugs = sanity["Bugs"];

  // construct the bugs table
   $('#bugs-info-table').DataTable({
    "data": bugs,
    columns : [
      
      {
        data: "Bug id",
        render: function (data, type, full, meta) {
          return data;
        }
      },
      
      {
        data: "Description",
        render: function (data, type, full, meta) {
          return data;
        }
      },
      {
        data: "Link",
        render: function (data, type, full, meta) {
          return "<a href=" + data + ">Bug details</a>" 
          //return data;
        }
      },
      {
        data: "Assignee",
        render: function (data, type, full, meta) {
          return data;
        }
      }
    ]
  });

} 

$(document).ready( function () {
  getSanity();  
});

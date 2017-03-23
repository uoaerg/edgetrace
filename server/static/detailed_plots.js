function drawCrates (){
    /*$.ajax({
      url: "../Plots/",
      success: function(data){
         $(data).find("a:contains(.jpg)").each(function(){
            // will loop through 
            var images = $(this).attr("href");

            $('<p></p>').html(images).appendTo('imageDiv')

         });
      }
    });*/
    
    document.getElementById("imageDiv_info").innerHTML = "Number of paths : " + numberofpaths + "<br>" + 
                                                            "Average number of hops per path : " + averagepathlength;

    var figure, figcaption, img, dscp;
    
    for(index in listofdscp){
        figure = document.createElement("figure");
        img = document.createElement("img");
        figcaption = document.createElement("figcaption");
        
        img.setAttribute("src", "generated/plots/Path_Information_DSCP" + listofdscp[index] + ".png");
        
        if (listofdscp[index] in listOfMeaning){
            dscp = listofdscp[index] + " (" + listOfMeaning[listofdscp[index]] + ")";
        }
        else{
            dscp = listofdscp[index]
        }
        img.setAttribute("title", "Initial DSCP " + dscp);
        
        
        figcaption.innerHTML = "Initial DSCP " + dscp;
        
        figure.appendChild(figcaption);
        figure.appendChild(img);
        document.getElementById("imageDiv").appendChild(figure);
    }
}
drawCrates();

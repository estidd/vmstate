# vmstat

1.the gui should be hosted on a LAN accesable web server

2.the python script will generate a pull on the APIC (variables can be changed in script)

3.the python script will output a xml file that the html gui will read in to display vmstats

4.installation in ACI dashboard is done through a modified app called visudash. You can edit this with your web server using 7zip and open up the visudash installer. You will see a main HTML page you can edit to point at your web server.


*Note that you will need to change the API call in the python script to specify your VM cluster

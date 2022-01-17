# Breitbandmessung.de automated

A script to enable customers of lazy ISPs to perform measurement campaigns of the connection speed as described [here](https://www.bundesnetzagentur.de/DE/Sachgebiete/Telekommunikation/Unternehmen_Institutionen/Breitband/Breitbandmessung/start.html) in an automated way.

## Usage

Create a `config` folder and a `config.cfg` file.

Example config.cfg:
```
timezone=Europe/Berlin
crontab=* */2 * * *
run_once=true
run_on_startup=true
```

Create a folder for the measurement results `mkdir messprotokolle`.

For the cronjob you can use [this website](https://crontab-generator.org/).
By default the measurement runs every 2 hours.

Timezone name from [this list](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List).
The default timezone is UTC.

The broadband measurement can run once or automated via cron.
For a one-time measurement set the value in the config to true.



Just run:

```
git clone https://github.com/shneezin/breitbandmessung.git && cd breitbandmessung
sudo ./create.sh alpine or debian
```
The Debian Container is available for the amd64, arm64 or arm/v/7 architecture.
The Alpine Container is available for the amd64 and arm64 architecture.

or 

```
docker run -d -v $PWD/config/:/usr/src/app/config:rw -v $PWD/messprotokolle:/export/ --name "breitbandmessung" shneezin/breitbandmessung
```
for the Alpine Container. __

If you want to use the Debian Container, use the following command:
```
docker run -d -v $PWD/config/:/usr/src/app/config:rw -v $PWD/messprotokolle:/export/ --name "breitbandmessung" shneezin/breitbandmessung:debian
```

To merge the csv files into one, run merge.sh or:
```
wget -O - https://raw.githubusercontent.com/shneezin/breitbandmessung/master/merge.sh | bash
```

## License

Feel free to use and improve the script as you like. I take no responsibility for the script.

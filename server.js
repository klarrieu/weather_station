const http = require('http');
const fs = require('fs');
const sqlite3 = require('sqlite3').verbose();


// connect to sqlite database
let db = new sqlite3.Database('/home/pi/Documents/weather_station/weather.db', sqlite3.OPEN_READONLY, (err) => {
  if (err) {
    console.error(err.message);
  }
  console.log('Connected to the weather database.');
});

// get data from database
var sql = `SELECT ts as ts, air_temp as air_temp, air_pressure as air_pressure, humidity as humidity, aqi as aqi, pm2_5 as pm2_5, pm10 as pm10 FROM weather WHERE ts >= datetime(CURRENT_TIMESTAMP, 'localtime', '-1 day');`;

var tss = [];
var air_temps = [];
var air_pressures = [];
var humidities = [];
var aqis = [];
var pm2_5s = [];
var pm10s = [];

var update = {};

var records = [];


function init_data(){
  return new Promise(resolve=>{
    tss = [];
    air_temps = [];
    air_pressures = [];
    humidities = [];
    aqis = [];
    pm2_5s = [];
    pm10s = [];
    db.all(sql, [], (err, rows) => {
      if (err) {
        throw err;
      }
      rows.forEach((row) => {
        // console.log(row.ts, row.air_temp, row.air_pressure, row.humidity, row.aqi, row.pm2_5, row.pm10);
        tss.push(row.ts);
        air_temps.push(row.air_temp);
        air_pressures.push(row.air_pressure);
        humidities.push(row.humidity);
        aqis.push(row.aqi);
        pm2_5s.push(row.pm2_5);
        pm10s.push(row.pm10);
      });
      resolve(tss, air_temps, air_pressures, humidities, aqis, pm2_5s, pm10s);
    });
  });
}

var latest_ts;
var sql_update;

function update_data(){
  return new Promise(resolve=>{
    if (Object.keys(update).length > 0){latest_ts = update.ts};
    update = {};
    console.log('checking for update, last ts:', latest_ts);
    sql_update = `SELECT ts as ts, air_temp as air_temp, air_pressure as air_pressure, humidity as humidity, aqi as aqi, pm2_5 as pm2_5, pm10 as pm10 FROM weather WHERE ts > \'${latest_ts}\';`;
    db.all(sql_update, [], (err, rows) => {
      if (err) {
        throw err;
      }
      // get new data to send as update
      if (tss.length > 0){
        rows.forEach((row) => {
          // console.log(row.ts, row.air_temp, row.air_pressure, row.humidity, row.aqi, row.pm2_5, row.pm10);
          update = {...row};
        });
      }
      resolve(update);
    });
  });
}


// create http server
const server = http.createServer((req, res) => {
  res.writeHead(200, { 'content-type': 'text/html' })
  fs.createReadStream('index.html').pipe(res)
});

// attach websocket to http server
const io = require('socket.io')(server);
io.on('connection', client => {
  console.log("websocket on...");
  client.emit('announcements', { message: 'Hello from the server!' });

  // send database data to webpage via websocket
  async function asyncInit(){
    records = await init_data();
    client.emit('data', {tss: tss,
                         air_temps: air_temps,
                         air_pressures: air_pressures,
                         humidities: humidities,
                         aqis: aqis,
                         pm2_5s: pm2_5s,
                         pm10s: pm10s
                        });
  };
  asyncInit();

  client.on('event', data => {console.log("received data: ${data}")
  });
  client.on('disconnect', () => {console.log("websocket disconnected.")
  });
});

// initialize latest_ts when server turns on
async function server_ts_init(){
  records = await init_data();
  latest_ts = tss.slice(-1)[0];
};
server_ts_init();

// periodically retrieve new data and send to clients
setInterval(() => {
  async function asyncUpdate(){
    records = await update_data();
    if (Object.keys(update).length > 0){
      console.log('got new data:', update);
      io.sockets.emit('update', {update: update})
    }
  };
  asyncUpdate();
  }, 20 * 1000);

// start listening
server.listen(8000);
console.log("Listening on port 8000");

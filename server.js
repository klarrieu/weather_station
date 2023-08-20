const http = require('http');
const fs = require('fs');
const sqlite3 = require('sqlite3').verbose();
const express = require('express');

// read device configs
let raw_config = fs.readFileSync('config.json');
let config = JSON.parse(raw_config);
var pars = [];
console.log('Device configs:');
for (device of config.installed_devices){
	console.log(device);
	console.log(config.device_configs[device]);
	pars = pars.concat(config.device_configs[device].params);
};

// connect to sqlite database
let db = new sqlite3.Database('./weather.db', sqlite3.OPEN_READONLY, (err) => {
  if (err) {
    console.error(err.message);
  }
  console.log('Connected to the weather database.');
});

// get data from database
var pars_as = pars.map(par => `${par} as ${par}`).join(', ')
var sql = `SELECT ts as ts, ${pars_as} FROM weather WHERE ts >= datetime(CURRENT_TIMESTAMP, 'localtime', '-1 day');`;

var tss = [];
//var air_temps = [];
//var air_pressures = [];
//var humidities = [];
//var aqis = [];
//var pm2_5s = [];
//var pm10s = [];
var par_arrays = {};
for (par of pars){
  par_arrays[par] = []
};

var update = {};

var records = [];


function init_data(){
  return new Promise(resolve=>{
    // re-initialize arrays
    tss= []
    for (par of pars){
      par_arrays[par] = []
    };
    // get data from sql db
    db.all(sql, [], (err, rows) => {
      if (err) {
        throw err;
      }
      rows.forEach((row) => {
        // console.log(row.ts, row.air_temp, row.air_pressure, row.humidity, row.aqi, row.pm2_5, row.pm10);
        tss.push(row.ts);
        //air_temps.push(row.air_temp);
        //air_pressures.push(row.air_pressure);
        //humidities.push(row.humidity);
        //aqis.push(row.aqi);
        //pm2_5s.push(row.pm2_5);
        //pm10s.push(row.pm10);
	for (par of pars){
          par_arrays[par].push(row[par])
        };
      });
      resolve(tss, par_arrays);
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
    sql_update = `SELECT ts as ts, ${pars_as} FROM weather WHERE ts > \'${latest_ts}\';`;
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
  if (req.url == "/"){
    res.writeHead(200, { 'content-type': 'text/html' });
    fs.createReadStream('./static/index.html').pipe(res)
  }
  else if (req.url == '/style.css'){
    res.writeHead(200, {'content-type': 'text/css'});
    fs.createReadStream('./static/style.css').pipe(res)
  }
  else if ((req.url == '/weather-update/') & (req.method == 'POST')){
    console.log('Heard POST request:');
    req.on('data', function (data) {
      console.log("got data:");
      var data = JSON.parse(data);
      console.log(data);
    });
    // var post = JSON.parse(body);
    // deal_with_post_data(request,post);
    // console.log(post);
    res.writeHead(200, {'content-type': 'text/html'});
    res.end();
  };
});

// attach websocket to http server
const io = require('socket.io')(server);
io.on('connection', client => {
  console.log("websocket on...");
  client.emit('announcements', { message: 'Hello from the server!' });

  // send database data to webpage via websocket
  async function asyncInit(){
    records = await init_data();
    client.emit('data', Object.assign({}, {tss: tss}, par_arrays));
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

'use strict';
// #region Algemeen
//const IP = prompt('geef publiek IP', 'http://127.0.0.1:5000');
//const IP = window.location.hostname + 'http://169.254.10.1:5000';
let socket;
let state;
let car;

console.log('test');
let lanIP = '169.254.10.1';

const getsocketconnection = function() {
  socket = io(window.location.host + ':5000');
  console.log('blejtn');
  setInterval(livedata, 5500);

  socket.on('giveAuto', function(data) {
    console.log(data);
    console.log(auto);
    if (data > 0.0) {
      console.log('bluvvn blejtn');
      const car = document.querySelector('.js-car');
      car.setAttribute('style', 'fill: red');
    } else {
      console.log('stopn me blejtn');
      const car = document.querySelector('.js-car');
      car.setAttribute('style', 'fill: green');
    }
  });
};

// const test = function() {
//  const car = document.querySelector('.js-car');
//  car.setAttribute('style', 'fill: red');
//  cargreen.setAttribute('style', 'fill: green');
// };

const livedata = function() {
  socket.emit('getAuto');
};

const init = function() {
  getsocketconnection();
  car = document.querySelector('#auto');
};

document.addEventListener('DOMContentLoaded', function() {
  console.info('DOM geladen');
  init();
});

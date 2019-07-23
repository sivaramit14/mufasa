var time = require('time');
exports.handler = (event, context, callback) => {
    var currentTime = new time.Date(); 
    currentTime.setTimezone("Europe/Copenhagen");
    callback(null, {
        statusCode: '200',
        body: 'The Time in Copenhagen is : ' + currentTime.toString(),
    });
};

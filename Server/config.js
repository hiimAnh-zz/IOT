const config = {
    app: {
        port: 3000,
        ip: "localhost"
    },
    db: {
        host: 'localhost',
        port: 27017,
        user: "root",
        password: "1234",
        database: "data_sensors", 
        name: 'Sensors',
        timeRefresh: 4000
    },
    mqtt: {
        server: "mqtt://localhost",
    }
};
module.exports = config;
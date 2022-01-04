require('dotenv').config();
const morgan = require('morgan');
const cors = require('cors');
const express = require('express');
const apiRouter = require('./routes/ApiRouter');

// initialization
const app = express();

// CORS
app.use(cors());

// morgan
app.use(morgan('dev'));

// body parsing
app.use(express.json());

// mongodb init
const db = require('./models/index');
console.log(db.url);
db.mongoose
  .connect(db.url, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
    useFindAndModify: false,
    useCreateIndex: true,
  })
  .then(() => {
    console.log('Connected to the database!');
  })
  .catch((err) => {
    console.log('Cannot connect to the database!', err);
    process.exit();
  });

// routing
app.use('/api/v1', apiRouter);

// server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`I love you ${PORT}`);
});

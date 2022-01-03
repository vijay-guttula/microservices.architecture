const morgan = require('morgan');
const cors = require('cors');
const express = require('express');
const apiRouter = require('./routes/ApiRouter');
const mongoose = require('mongoose');

// initialization
const app = express();

// CORS
app.use(cors());

// morgan
app.use(morgan('dev'));

// body parsing
app.use(express.json());

// mongodb init
const connString = process.env.MONGODB_CONNSTRING;
mongoose.connect(
  connString,
  {
    useNewUrlParser: true,
    useUnifiedTopology: true,
    useFindAndModify: false,
    useCreateIndex: true,
  },
  () => {
    console.log('Database Connected');
  }
);

// routing
app.use('/api/v1', apiRouter);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`I love you ${PORT}`);
});

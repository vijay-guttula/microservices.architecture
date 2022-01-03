const express = require('express');
const apiRouter = express.Router();
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
// const secret = process.env.secret;

apiRouter.get('/users', async (req, res) => {
  console.log('hi');
});

module.exports = apiRouter;

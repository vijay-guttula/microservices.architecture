require('dotenv').config();
const express = require('express');
const apiRouter = express.Router();
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const db = require('../models/index');
const User = db.users;
const secret = process.env.secret;
const publish = require('../workers/producer');

// user sign up
apiRouter.post('/auth/signup', async (req, res) => {
  const { firstName, lastName, phoneNumber, email, password } = req.body;
  const checkDuplicate = await User.findOne({ email });
  if (checkDuplicate) {
    res.status(500).json({
      message: 'User Already exists with the email',
    });
    return;
  }
  const salt = await bcrypt.genSalt(10);
  const secretPassword = await bcrypt.hash(password, salt);

  // adding the user to the database
  const user = await User.create({
    firstName,
    lastName,
    phoneNumber,
    email,
    password: secretPassword,
  });
  console.log(user);
  var token = jwt.sign({ id: user._id }, secret, {
    expiresIn: 86400,
  });
  await publish(`${email}`);
  res.status(201).json({
    message: 'User Created Successfully',
    data: user,
    accessToken: token,
  });
});

// user login
apiRouter.post('/auth/login', async (req, res) => {
  const { email, password } = req.body;
  const findUser = await User.findOne({ email });
  console.log(findUser);
  if (findUser) {
    const checkPassword = await bcrypt.compareSync(password, findUser.password);
    if (checkPassword) {
      var token = jwt.sign({ id: findUser._id }, secret, {
        expiresIn: 86400,
      });
      res.status(200).json({
        message: 'User login successfull',
        data: findUser,
        accessToken: token,
      });
      return;
    }
    res.status(500).json({
      for: 'password',
      message: 'Wrong password entered',
    });
    return;
  }
  res.status(501).send({
    for: 'email',
    message:
      "'No user with the entered email is present, please create your account'",
  });
});

// // user edit
// apiRouter.put('/users:userId')

module.exports = apiRouter;

require('dotenv').config();
const express = require('express');
const apiRouter = express.Router();
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const db = require('../models/index');
const User = db.users;
const secret = process.env.secret;
const publish = require('../workers/producer');

// middlewares
apiRouter.use('/users', async (req, res, next) => {
  const { email } = req.body;
  const findUser = await User.findOne({ email });
  if (!findUser) {
    res.status(501).send({
      for: 'email',
      message:
        "'No user with the entered email is present, please create your account'",
    });
    return;
  }
  next();
});

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
  await publish({
    operation: 'user_created',
    email_id: email,
  });
  res.status(201).json({
    message: 'User Created Successfully',
    data: user,
    accessToken: token,
  });
});

// user login
apiRouter.post('/auth/login', async (req, res) => {
  const { email, password } = req.body;
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
});

// user delete
apiRouter.delete('/users', async (req, res) => {
  const { email } = req.body;
  const deleteUser = await User.findOneAndDelete({ email });
  if (deleteUser) {
    publish({
      operation: 'user_deleted',
      email_id: email,
    });
    res.status(204).json({
      message: 'User Deleted successfully',
    });
    return;
  }
});

module.exports = apiRouter;

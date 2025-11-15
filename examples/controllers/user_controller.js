/**
 * User Controller
 * Handles all user-related HTTP requests
 */

const express = require('express');
const router = express.Router();

// Get all users
router.get('/api/users', async (req, res) => {
    const users = await User.findAll();
    res.json(users);
});

// Create new user
router.post('/api/users', async (req, res) => {
    const user = await User.create(req.body);
    res.status(201).json(user);
});

// Get user by ID
router.get('/api/users/:id', async (req, res) => {
    const user = await User.findById(req.params.id);
    if (!user) {
        return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
});

// Update user
router.put('/api/users/:id', async (req, res) => {
    const user = await User.update(req.params.id, req.body);
    res.json(user);
});

// Delete user
router.delete('/api/users/:id', async (req, res) => {
    await User.delete(req.params.id);
    res.status(204).send();
});

// Get user posts
router.get('/api/users/:id/posts', async (req, res) => {
    const posts = await Post.findByUserId(req.params.id);
    res.json(posts);
});

module.exports = router;

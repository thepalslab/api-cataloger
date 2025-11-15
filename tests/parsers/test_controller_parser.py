"""Tests for controller parser."""
import pytest
from pathlib import Path
from api_cataloger.parsers.controller_parser import ControllerParser


@pytest.fixture
def controller_parser():
    return ControllerParser()


@pytest.fixture
def express_controller(tmp_path):
    """Create a sample Express controller file."""
    content = """
const express = require('express');
const router = express.Router();

router.get('/api/users', (req, res) => {
    res.json({ users: [] });
});

router.post('/api/users', (req, res) => {
    res.status(201).json(req.body);
});

module.exports = router;
"""
    file_path = tmp_path / "user_controller.js"
    file_path.write_text(content)
    return file_path


@pytest.fixture
def flask_controller(tmp_path):
    """Create a sample Flask controller file."""
    content = """
from flask import Blueprint, jsonify

bp = Blueprint('api', __name__)

@bp.route('/api/products', methods=['GET'])
def get_products():
    return jsonify([])

@bp.route('/api/products', methods=['POST'])
def create_product():
    return jsonify({}), 201
"""
    file_path = tmp_path / "product_controller.py"
    file_path.write_text(content)
    return file_path


def test_can_parse_controller(controller_parser, express_controller):
    """Test that parser can identify controller files."""
    assert controller_parser.can_parse(express_controller) is True


def test_cannot_parse_non_controller(controller_parser, tmp_path):
    """Test that parser rejects non-controller files."""
    non_controller = tmp_path / "model.py"
    non_controller.write_text("class User:\n    pass")
    assert controller_parser.can_parse(non_controller) is False


def test_parse_express_controller(controller_parser, express_controller):
    """Test parsing Express controller."""
    entry = controller_parser.parse(express_controller)
    
    assert entry is not None
    assert len(entry.endpoints) == 2
    
    get_endpoint = next(ep for ep in entry.endpoints if ep.method == "GET")
    assert get_endpoint.path == "/api/users"
    
    post_endpoint = next(ep for ep in entry.endpoints if ep.method == "POST")
    assert post_endpoint.path == "/api/users"


def test_parse_flask_controller(controller_parser, flask_controller):
    """Test parsing Flask controller."""
    entry = controller_parser.parse(flask_controller)
    
    assert entry is not None
    assert len(entry.endpoints) == 2
    
    # Check that both endpoints were found
    methods = [ep.method for ep in entry.endpoints]
    assert "GET" in methods
    assert "POST" in methods

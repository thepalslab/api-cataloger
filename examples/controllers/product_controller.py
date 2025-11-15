"""
Product API Controller
Manages product catalog and inventory
"""

from flask import Blueprint, jsonify, request
from models import Product

blueprint = Blueprint('products', __name__)


@blueprint.route('/api/products', methods=['GET'])
def get_products():
    """Get all products with optional filtering."""
    category = request.args.get('category')
    products = Product.query.filter_by(category=category) if category else Product.query.all()
    return jsonify([p.to_dict() for p in products])


@blueprint.route('/api/products', methods=['POST'])
def create_product():
    """Create a new product."""
    data = request.get_json()
    product = Product(**data)
    product.save()
    return jsonify(product.to_dict()), 201


@blueprint.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID."""
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())


@blueprint.route('/api/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    """Update an existing product."""
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    product.update(**data)
    return jsonify(product.to_dict())


@blueprint.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product."""
    product = Product.query.get_or_404(product_id)
    product.delete()
    return '', 204


@blueprint.route('/api/products/<product_id>/inventory', methods=['GET'])
def get_inventory(product_id):
    """Get inventory levels for a product."""
    product = Product.query.get_or_404(product_id)
    return jsonify(product.get_inventory())

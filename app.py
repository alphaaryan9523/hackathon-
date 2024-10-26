from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from ml_model import predict_demand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Import models
from models import Inventory, Supplier

# Routes for inventory management
@app.route('/inventory', methods=['GET', 'POST'])
def manage_inventory():
    if request.method == 'POST':
        data = request.json
        new_item = Inventory(
            name=data['name'],
            quantity=data['quantity'],
            barcode=data['barcode'],
            serial_number=data.get('serial_number'),
            supplier_id=data['supplier_id']
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"message": "Item added successfully"}), 201

    inventory = Inventory.query.all()
    return jsonify([item.to_dict() for item in inventory])

# Route for supplier management
@app.route('/suppliers', methods=['GET', 'POST'])
def manage_suppliers():
    if request.method == 'POST':
        data = request.json
        new_supplier = Supplier(name=data['name'], lead_time=data['lead_time'])
        db.session.add(new_supplier)
        db.session.commit()
        return jsonify({"message": "Supplier added successfully"}), 201

    suppliers = Supplier.query.all()
    return jsonify([supplier.to_dict() for supplier in suppliers])

# Route for demand prediction
@app.route('/predict_demand', methods=['POST'])
def demand_prediction():
    data = request.json['historical_data']  # Pass historical inventory levels
    prediction = predict_demand(data)
    return jsonify({"forecast": prediction})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

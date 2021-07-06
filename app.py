import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_monitoringdashboard as dashboard

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///rantanplan"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
dashboard.bind(app)

from models import Place, Operation, Signals

@app.route("/place/signal", methods=['POST'])
def handle_place():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()

            new_place = Place( 
                            place_name=data['place_name'], 
                            place_address=data['place_address']
                            )

            db.session.add(new_place)
            db.session.commit()

            new_operation = Operation( 
                                    place_id=new_place.id,
                                    start_time=data['start_time'], 
                                    end_time=data['end_time'],
                                    round_count=data['round_count'],
                                    )

            db.session.add(new_operation)
            db.session.commit()

            signals = data.get('signals')
            for new_signal in signals:
                new_signal = Signals(
                                    operation_id=new_operation.id,
                                    bssid=new_signal['bssid'], 
                                    ssid=new_signal['ssid'],
                                    frequency=new_signal['frequency'],
                                    signal_level=new_signal['signal_level'],
                                    sample_count=new_signal['sample_count']
                                    )
                db.session.add(new_signal)

        
            db.session.commit()
            
            
            return {"respone": "place_id: {}".format(new_place.id)}
        else:
            return {"error": "The request payload is not in JSON format"}


@app.route('/place/<place_id>/signal', methods=['POST'])
def handle_place_id(place_id):

    place = Place.query.get_or_404(place_id)

    if request.method == 'POST':
        data = request.get_json()
        place.place_name = data['place_name']
        place.place_address = data['place_address']
        db.session.add(place)
        db.session.commit()
        
        operation = Operation( 
                            place_id=place.id,
                            start_time=data['start_time'], 
                            end_time=data['end_time'],
                            round_count=data['round_count'])
        db.session.add(operation)
        db.session.commit()

        signals=data.get('signals')
        for signal in signals:
            signal = Signals(
                operation_id=operation.id,
                bssid=signal['bssid'], 
                ssid=signal['ssid'],
                frequency=signal['frequency'],
                signal_level=signal['signal_level'],
                sample_count=signal['sample_count']
            )

        db.session.add(signal)
        db.session.commit()

        return {"message": "place_id: {} successfully updated".format(place_id)}


@app.route('/place/search', methods=['POST'])
def search():

    if request.method == "POST":
        data = request.get_json()
        
        signals = data.get('signals')
        
        result_place = Place.query.all()
        result_operation = Operation.query.all()
        result_signals = Signals.query.all()

        for result in result_place:
            id_place = result.id
            place_name = result.place_name
            place_address = result.place_address
            

        for result in result_operation:
            id_operation = result.id
            place_id = result.place_id
        

        for result in result_signals:
            operation_id = result.operation_id
            bssid = result.bssid
            signal_level = result.signal_level

        

        result_dict={}
        if (id_place==place_id and id_operation==operation_id):
            id = id_place
            name = place_name
            address = place_address
            bssid = bssid
            level = signal_level
            if id_place in result_dict:
                result_dict[id_place][bssid] = level
            else:
                result_dict[id] = { bssid : level, "name" : name, "address" : address}

        result_score = []

        for place_id in result_dict:
            score = 100
            for signal in signals:
                bssid = signal['bssid']
                if (bssid not in result_dict[place_id]) or (abs(signal['signal_level'] - result_dict[place_id][bssid]) > 20):
                    score -= (100 //len(signals))
                    if score < 50:
                        score = -1
                        break
            result_score.append({
                'place_id' : place_id,
                'place_name' : result_dict[place_id]['name'],
                'place_address' : result_dict[place_id]['address'],
                'score' : score
            })

        return {"place":result_score}
        

if __name__ == '__main__':
    app.run()
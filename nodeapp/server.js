const express = require('express');
const cors = require('cors');
const app = express(); app.use(cors()); app.use(express.json());
const dealers = [
{id:1, city:'New York', state:'New York', address:'123 Broadway', zip:'10001', lat:40.7128, long:-74.0060, short_name:'Best Cars NY', full_name:'Best Cars of New York'},
{id:15, city:'Wichita', state:'Kansas', address:'123 Main Street', zip:'67201', lat:37.6872, long:-97.3301, short_name:'Best Cars KS', full_name:'Best Cars Kansas'},
{id:16, city:'Topeka', state:'Kansas', address:'789 Kansas Ave', zip:'66603', lat:39.0473, long:-95.6752, short_name:'Auto Kansas', full_name:'Auto Kansas Dealership'}
];
const reviews = [{dealerId:15, name:'John Smith', review:'Fantastic services', purchase:true, car_make:'Toyota', car_model:'Camry'}];
app.get('/fetchDealers', (req,res)=>res.json({dealers}));
app.get('/fetchDealers/:state', (req,res)=>res.json({dealers: dealers.filter(d=>d.state.toLowerCase()===req.params.state.toLowerCase())}));
app.get('/fetchDealer/:id', (req,res)=>res.json(dealers.find(d=>d.id==req.params.id)||{}));
app.get('/fetchReviews/dealer/:id', (req,res)=>res.json({dealerId:Number(req.params.id), reviews: reviews.filter(r=>r.dealerId==req.params.id)}));
app.listen(3030, ()=>console.log('Dealer service running on port 3030'));

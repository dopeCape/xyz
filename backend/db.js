const mongoose = require("mongoose")
mongoose.connect("mongodb+srv://swaraj:Swaraj2004@cluster0.txvw2vk.mongodb.net/PayTm-Clone")

const userSchema = mongoose.Schema({
    username:String,
    firstName:String,
    lastName:String,
    password:String
})

const accountSchema = mongoose.Schema({
    userId: {
        type: mongoose.Schema.Types.ObjectId, 
        ref: 'User',
        required: true
    },
    balance:Number

})

const User = mongoose.model('User',userSchema)
const Account = mongoose.model('Account',accountSchema)
module.exports={User,Account}
const mongoose = require("mongoose")
mongoose.connect("")

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
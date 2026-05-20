
module.exports.sendEmail = async (event) => {

    return {
        statusCode: 200,
        body: JSON.stringify({
            message: "Email service working successfully"
        })
    };

};

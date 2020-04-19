db.createUser({
    user: "adoptacutie",
    pwd: "NicePasswordM8",
    roles: [
        {
            role: "readWrite",
            db: "adoptacutie"
        }
    ]
});
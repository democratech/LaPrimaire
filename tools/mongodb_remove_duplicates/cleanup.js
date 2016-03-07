db.Signature.renameCollection("supporteurs");
db.Commune.renameCollection("communes");
db.supporteurs.remove({"created": {"$lt": ISODate("2015-06-23T06:05:51Z")}});
var keys = {};
db.supporteurs.find().forEach(function(doc) {
	var key=doc.email;
	if (keys[key]) {
		db.supporteurs.remove({_id: doc._id});
	} else {
		keys[key] = true;
	}
});
db.supporteurs.createIndex({email: 1}, {unique: true});

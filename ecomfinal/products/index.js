useEffect(() =>
{
	const unsubscribe = auth.onAuthStateChanged((authUser) =>{
		if (authUser) {
			console.log(authUser);
			setUser(authUser);
			if (authUser.displayName) {
				// Dont update username
			}
			else{
				// if we just created someone
				return authUser.updateProfile({
					displayName:username,
				});
			}
		}
		else{
			setUser(null)
		}
	})


	return () =>{
		unsubscribe();
	}
},[user , username);

{
	user ? (
		<Button onClick={() => auth.signOut()}>
			Logout
		</Button>
		):(
			<Button onClick={() => setOpen(true)}>
			Sign Up
		</Button>
		)
}

const handleChange =(e) =>{
	if(e.target.files[0]){
		setImage(e.target.files[0])
	}
}

const handleUpload = () =>{
	const uploadTask = storage.ref(`images/${image.name}`).put(image)

	uploadTask.on(
		'state_changed',
		(snapshot) =>{
			// progress function
			const progress = Math.round(
				(snapshot.bytesTransfered / snapshot.totalBytes)*100
			);
			setProgress(progress);
		}
	)
},
() =>{
	// Complete the function
	storage
		.ref('images')
		.child(image.name)
		.getDownloadURL()=>{
			collection(db , 'posts').add({
				timestamp:firebase.firestore.FieldValue.serverTimestamp()
			})
		}
		.then(url)
}

{
	user?.displayName ? (
		<ImageUpload username = {user.displayName} />
		):(

			<h3>Login to Uplad</h3>
		)
}



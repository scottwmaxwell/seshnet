const observer = new IntersectionObserver((entries) =>{
	entries.forEach((entry) => {
		console.log(entry)
		if (entry.isIntersecting){
			entry.target.classList.add('show');
		} else {
			entry.target.classList.remove('show');
		}
	});
});

const observer2 = new IntersectionObserver((entries) =>{
	entries.forEach((entry) => {
		console.log(entry)
		if (entry.isIntersecting){
			entry.target.classList.add('showing');
		} else {
			entry.target.classList.remove('showing');
		}
	});
});

const hiddenElements = document.querySelectorAll('.hidden');
console.log(hiddenElements)
hiddenElements.forEach((el) => observer.observe(el));

const hidingElements = document.querySelectorAll('.hiding');
console.log()
hidingElements.forEach((el) => observer2.observe(el));




fetch("https://api.collegefootballdata.com/teams/fcs")
    .then(res => res.json())
    .then(res => {
        // console.log(res.school);
        let x = Math.floor(Math.random() * res.length);
        console.log(x)
        let school = res[x]
        console.log(school)
        document.getElementById("school").src = school.logos[0]
        document.getElementById("school").alt = school.school
        document.getElementById("name").innerHTML = school.school
    })
        .catch(err => console.log(err))

for (var i=1; i<=255; i++{
    if (i%2 != 0){
        arr.push(i);
    }
    return arr;
})


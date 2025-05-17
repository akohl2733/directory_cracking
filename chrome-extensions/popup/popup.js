const container = document.createElement("div");
container.id = "extension-container";
document.body.appendChild(container);

document.getElementById("submit").addEventListener("click", () => {
    const name = document.getElementById("name").value.trim();
    const title = document.getElementById("title").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim();

    if (!name | !title | !email | !phone) {
        alert("Please fill out all fields.");
        return;
    }

    const entry = {name, title, email, phone};

    fetch("universityscraper-gqasazcshnd9e8a8.canadacentral-01.azurewebsites.net/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({ entries: [entry] })
    })
    .then(res => res.json())
    .then(Data => {
        if (Data.status === "success") {
            alert("Contact has been successfully added to the database!")
            document.getElementById('name').value = "";
            document.getElementById('title').value = "";
            document.getElementById('email').value = "";
            document.getElementById('phone').value = "";
        } else {
            alert("There was an error submitting the data.")
        }
    })
    .catch(err => {
        console.error("Submission error:". err);
        alert("Submission failed.")
    })
});

// Clear the Manual Input Fields automatically
document.getElementById("clear-manual").addEventListener("click", () => {
    document.getElementById('name').value = "";
    document.getElementById('title').value = "";
    document.getElementById('email').value = "";
    document.getElementById('phone').value = "";
});

document.addEventListener("DOMContentLoaded", () => {
    chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
        const url = tabs[0].url;

        fetch("universityscraper-gqasazcshnd9e8a8.canadacentral-01.azurewebsites.net/scrape", {
            method: "POST",
            headers: { "Content-Type": "application/json"},
            body: JSON.stringify({url: url})
        })
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById("results");
            if (Array.isArray(data)) {
                data.forEach((person, index) => {
                    const personDiv = document.createElement("div");
                    personDiv.classList.add("contact");

                    // Create the contact card
                    personDiv.innerHTML = `<div class="indv">
                        <p style="font-weight:bolder;">${person.name}</p>
                        <p>${person.title}</p>
                        <p>${person.email}</p>
                        <p>${person.phone}</p>
                        <button id="submit-${index}">Submit Contact to Database</button>
                        </div>
                        <hr></hr>   
                    `;
                    resultsDiv.appendChild(personDiv);  

                    document.getElementById(`submit-${index}`).addEventListener("click", () => {
                        const indvDiv = personDiv.querySelector(".indv");
                        const submitBtn = document.getElementById(`submit-${index}`);
                        submitBtn.disabled = true;
                        submitBtn.textContent = "Submitted";
                        submitBtn.style.cursor = "not-allowed";
                        submitBtn.style.opacity = "0.6";  // optional: visually gray it out
                        indvDiv.style.backgroundColor = "lightgray";
                        fetch("universityscraper-gqasazcshnd9e8a8.canadacentral-01.azurewebsites.net/submit", {
                            method: "POST",
                            headers: {"Content-Type": "application/json"},
                            body: JSON.stringify({entries: [person]})
                        })
                        .then(res => res.json())
                        .then(data => {
                            if (data.status === "success") {
                                alert(`Successfully submitted ${person.name}`);
                            } else {
                                alert(`We were not able to submit ${person.name}`);
                            }
                        })
                        .catch(err => {
                            console.error("Submission error:", err);
                            alert("Submission failed.")
                        })
                    })
                });
            } else {
                resultsDiv.innerHTML = "<p>NO contacts found or error occurred.</p>";
            }
        })
        .catch(err => {
            console.error("Scraping error:", err);
            document.getElementById("results").innerHTML = "<p>Failed to fetch contacts.</p>";
        });
    });
});
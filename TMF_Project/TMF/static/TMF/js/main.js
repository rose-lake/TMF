const main = document.querySelector('main');
// console.log('main', main);
// console.log('main.getAttribute("data-page")', main.getAttribute('data-page'));

// run this code only if we are on the article-detail page:
if (main.getAttribute('data-page') == 'article-detail') {
    const shuffle_button = document.getElementById('shuffle-quotes');

    shuffle_button.addEventListener("click", () => {

        var my_quotes = document.querySelector('.my-quotes');
        for (var i = my_quotes.children.length; i >= 0; i--) {
            // take an existing child randomly chosen, by index,
            // and append it to the end of the list.
            // the loop decrements the "i" each time,
            // so that the RANGE for our randomly chosen index decreases each time.
            index = Math.floor(Math.random() * i);
            // this move swaps the 'shuffled' item to the back of the list.
            my_quotes.appendChild(my_quotes.children[index]);
        }

    });
}

// // TESTING THE SHUFFLE for SHUFFLE-y-ness
// // I tested the below version of the shuffle at
// // https://bost.ocks.org/mike/shuffle/compare.html
// // and it gave a good/balanced result:
//
// function shuffle(array) {
//     for (var i = array.children.length; i >= 0; i--) {
//         index = Math.floor(Math.random() * i);
//         array.appendChild(my_quotes.children[index]);
//     }
// }

// // implementation of Fisher-Yates shuffle, in-place version
// // thanks, https://bost.ocks.org/mike/shuffle/ !
// function shuffle(quotes) {
//     var m = quotes.length,
//         t, i;
//
//     // While there remain elements to shuffle…
//     while (m) {
//
//         // Pick a remaining element…
//         i = Math.floor(Math.random() * m--);
//
//         // And swap it with the current element.
//         t = quotes[m];
//         quotes[m] = quotes[i];
//         quotes[i] = t;
//     }
//
//     return quotes;
// }

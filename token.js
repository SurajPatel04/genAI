const text = "the cat sat on the mat    Embedding";
let tokens = [];
let hold = 1;

for (let i = 0; i < text.length; i++) {
  tokens.push(text.charCodeAt(i));
}

console.log(tokens);

const decodedText = tokens.map((code) => String.fromCharCode(code)).join("");

console.log("Decoded Text:", decodedText);

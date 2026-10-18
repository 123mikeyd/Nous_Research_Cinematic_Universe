'use strict';
const input = document.querySelector('#search');
const cards = [...document.querySelectorAll('.card')];
const normalize = value => value.normalize('NFKD').toLocaleLowerCase().replace(/[^a-z0-9]+/g, '');
function update() {
  const query = normalize(input.value);
  let count = 0;
  for (const card of cards) {
    card.hidden = !normalize(card.dataset.search).includes(query);
    if (!card.hidden) count++;
  }
  document.querySelector('#count').textContent = `${count} of ${cards.length} profiles`;
  document.querySelector('#empty').hidden = count !== 0;
}
function reset() { input.value = ''; update(); input.focus(); }
input.addEventListener('input', update);
input.addEventListener('keydown', event => { if (event.key === 'Escape') reset(); });
document.querySelector('#reset').addEventListener('click', reset);
document.querySelector('#empty-reset').addEventListener('click', reset);
update();

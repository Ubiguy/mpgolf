/* ============================================================
   MPG Winter Tournament 2027 season - ALL figures for winter-2027.html.
   Twelve Sundays, 15/11/2026 to 31/01/2027, Wike Ridge (January added 22/11/2026 at the owner's request).
   Points are Stableford NET (off handicap), as recorded in Golf GameBook.
   Champion: highest total of a player's best 6 rounds (all of them if 6 or fewer).

   To add a round:  python tools/winter_add_round.py  (see its top comment)
   or copy a block below by hand. Dates are DD/MM/YYYY. Names as in data.js.
   ============================================================ */
const WINTER_2027 = {
  title: 'Winter Tournament',
  course: 'Leeds Golf Centre, Wike Ridge',
  dates: ['15/11/2026','22/11/2026','29/11/2026','06/12/2026','13/12/2026','20/12/2026','27/12/2026',
          '03/01/2027','10/01/2027','17/01/2027','24/01/2027','31/01/2027'],
  countBest: 6,
  rounds: [
    { date: '15/11/2026', course: 'Wike Ridge', rows: [
      ['Tariq Javaid', 19, 37],
      ['Sid Amin', 12, 34],
      ['Imran K', 10, 33],
      ['Raz Shafi', 7, 32],
      ['Mahmood Sadiq', 13, 25],
      ['Shufqat Khan', 9, 22],
    ]},
    { date: '22/11/2026', course: 'Wike Ridge', rows: [
      ['Guftar Hussain', 4, 31],
      ['Yaseen Mohammed', 9, 30],
      ['Mansoor M', 12, 29],
      ['Imran K', 10, 27],
      ['Sid Amin', 12, 27],
      ['Waseem Goldenboy', 12, 27],
      ['Tariq Javaid', 19, 23],
      ['Shazad Hussain', 16, 22],
      ['Basharat Ali', 12, 21],
      ['Raz Shafi', 7, 20],
      ['Shufqat Khan', 9, 18],
    ]},
  ]
};

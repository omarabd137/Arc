"""Jason-Aufnahme v3: pro Kapitel ein Text mit eleven_v4-Regie-Tags. Beats getrennt durch [pause] (zum Schneiden an Pausen).
Reihenfolge der Beats je Kapitel = CH[k]['beats']."""
P = "\n\n[pause]\n\n"
CH = [
 dict(beats=["B0", "B1", "B2", "B3"], text=P.join([
  "[confident] [deep voice] This is a hundred-dollar bill. It costs less than TEN cents to make. [dramatically] And by the end of this video, this exact bill will make one man rich... and another man poor. [serious] Neither of them breaks a single rule. They both do exactly what they were taught.",
  "[warmly] Meet Jake. And Ryan. Same street. Same school. Same grades. [energetic] At twenty-five, they even get hired by the same company. Same desk. Same salary. Sixty thousand dollars a year.",
  "[slowly] Twenty years later...",
  "[dramatically] Ryan is a MILLIONAIRE. [serious] Jake is still renting... and still paying off a credit card. [confident] Ryan isn't smarter. He didn't inherit anything. He didn't get lucky. He just understood three things Jake never did. Where money actually comes from. Who gets it first. And why the same paycheck can make one person rich... and keep another one poor. [dramatically] Once you see it, you can never unsee it."])),
 dict(beats=["B5", "B6", "B7", "B8", "B9", "B10"], text=P.join([
  "[energetic] Let's follow the bill. Jake gets his first paycheck, and he does the responsible thing. He takes it to the bank.",
  "[mischievously] And here's the first thing nobody tells you. [confident] The moment that bill crosses the counter, it stops being Jake's. Legally, Jake just LENT his money to the bank. What he gets back isn't cash. It's a number in an app. [dramatically] A promise.",
  "[curious] Think of it like a coat check. You hand over your coat and get a little ticket. [mischievously] Except this coat check doesn't keep your coat. It lends it out to someone else while you're inside... and charges them for it.",
  "[energetic] Before Jake is even home, the bank has lent his money to a stranger buying a car. At eight percent interest. Jake earns almost nothing. The bank keeps the difference.",
  "[curious] So how much does the bank actually have to keep in the vault, in case Jake wants his money back? Since March 2020, in America, the legal requirement is... [dramatically] zero.",
  "[serious] Zero percent. If everyone asked for their money on the same day, it simply wouldn't be there. That's exactly what happened in the 1930s, when thousands of banks collapsed. Today, the government insures deposits up to two hundred fifty thousand dollars, so people stay calm. [mischievously] But that's not even the strangest part. [dramatically] The bank didn't even NEED Jake's bill to lend money. It can create money that never existed."])),
 dict(beats=["B11", "B12", "B13", "B13b", "B14", "B15"], text=P.join([
  "[energetic] Three years later, Ryan wants a house. He asks for a three-hundred-thousand-dollar mortgage.",
  "[curious] So where does that money come from? Not from a vault. Not from other customers' savings. [confident] The banker types it in. That's it. [dramatically] A second ago, that money did not exist. Now it does. [serious] And when Ryan pays the loan back, it disappears again.",
  "[confident] This isn't a conspiracy theory. The Bank of England published it in 2014. Most of the money in the modern economy is created by ordinary banks... whenever they make a loan.",
  "[curious] But wait. Isn't money backed by gold? It used to be. Until one Sunday evening in August 1971. [serious] President Nixon went on television and announced that the dollar would no longer be exchangeable for gold. Since that night, the dollar is backed by one thing only: trust. Trust that others will accept it. [dramatically] Which means there's no natural limit on how many dollars can be created.",
  "[energetic] That's why only about one in ten dollars in America exists as physical cash. The rest is numbers on screens, created by loans.",
  "[confident] And above the banks sits the Federal Reserve, the bank of the banks. Between 2020 and 2022, it created TRILLIONS of new dollars. Its balance sheet more than doubled, from about four trillion to almost nine. [dramatically] Which leads to a dangerous question. When all that new money appears... who gets it first?"])),
 dict(beats=["B16", "B17", "B18", "B19", "B19b"], text=P.join([
  "[curious] Picture a fountain. New money is poured in at the top. The people closest to it, banks, big investors, the already rich, drink first. [serious] By the time it trickles down to Jake... it's barely a drop.",
  "[confident] An economist named Richard Cantillon noticed this almost three hundred years ago. Whoever gets new money first spends it at the OLD prices. Whoever gets it last... pays the new ones.",
  "[energetic] In 2020, the amount of dollars in America grew by about twenty-five percent. In a single year. The money went into stocks and houses first. American home prices jumped by around forty percent in two years. [dramatically] American billionaires got more than a TRILLION dollars richer.",
  "[sarcastic] And Jake? Jake got a small raise. And much more expensive groceries. [mischievously] Which brings us to the tax nobody ever voted for.",
  "[serious] Here's the cruel part. Jake's boss gives him a three-percent raise, and Jake is grateful. The same month, his landlord raises the rent by eight. On paper, Jake earns more than ever. In reality, he can afford LESS than last year. [dramatically] Wages are always the last thing in line at the fountain."])),
 dict(beats=["B20", "B21", "B21b", "B22", "B23", "B24"], text=P.join([
  "[confident] This is what inflation really does. A hundred dollars from the year 2000 buys about what fifty-five did back then. Nobody took it out of your wallet. [softly] It just... quietly lost its power.",
  "[serious] Jake keeps his savings in the bank, earning less than half a percent. Prices rise about three percent a year. So Jake isn't really saving. [dramatically] He's losing. Slowly. Every single year.",
  "[curious] Remember the three questions? We now know where money comes from, and who gets it first. But the most important one is still open. Why did the same paycheck take these two in opposite directions? [mischievously] It started with one boring decision.",
  "[warmly] Ryan did something boring at twenty-five. Every month, before he spent anything, five hundred dollars went automatically into an index fund. A tiny piece of the five hundred biggest companies in America.",
  "[confident] Over the long run, the stock market has grown about ten percent a year on average. Not guaranteed, with crashes along the way. [dramatically] But look what time does. The same ten thousand dollars, left alone for twenty years: in Jake's savings account, about ten thousand eight hundred. In Ryan's fund, historically... around SIXTY-SEVEN thousand.",
  "[serious] Meanwhile, Jake did what felt normal. A new car. On a loan. The moment he drove it off the lot, it lost about a fifth of its value. Ryan's money bought things that grow. Jake's money bought things that shrink. [dramatically] And Jake's real trap was still coming."])),
 dict(beats=["B25", "B26", "B27", "B28", "B29", "B30"], text=P.join([
  "[energetic] One day, a letter arrives. [sarcastic] Congratulations. Jake is pre-approved. Ten thousand dollars of credit.",
  "[confident] Now look at the deal. The bank pays Jake less than half a percent on his savings. And charges him over TWENTY percent on his card. With money it can create by typing. [dramatically] Jake is on the losing side of every single trade.",
  "[serious] A five-thousand-dollar balance, paid back only at the minimum, can take more than ten years... and cost thousands in interest. It's not that Jake is stupid. Nobody ever showed him which side of the table he was sitting on. [mischievously] And the very rich? They sit on a side of the table most people don't even know exists.",
  "[curious] Imagine you own a billion dollars in stock. If you sell it, you pay tax. [mischievously] So... you don't sell.",
  "[confident] Instead, you borrow against your shares. A loan isn't income. No income, no income tax. Your stocks keep growing, faster than the interest. So you borrow again. [dramatically] Reporters at ProPublica gave this strategy a name: Buy. Borrow. Die.",
  "[warmly] Ryan isn't a billionaire. But he plays a small version of the same game. His loan bought a house that grew. His paycheck bought shares that grew. [serious] Jake's loans bought a car and a lifestyle. [mischievously] And when the biggest players lose... something even stranger happens."])),
 dict(beats=["B31", "B32", "B32b", "B33"], text=P.join([
  "[serious] In 2008, the biggest banks made reckless bets with borrowed money, and lost. [dramatically] They weren't allowed to fail. Seven hundred billion dollars of taxpayer money was approved to rescue the system.",
  "[confident] In 2023, Silicon Valley Bank collapsed. Every depositor got their money back, even the ones far above the insured limit. When they win, they keep the profits. When they lose, everyone else catches them. [sarcastic] Remember Jake's credit card at twenty percent? Nobody is coming to rescue that.",
  "[serious] And every time there's a crisis, the Federal Reserve does the same thing. It cuts interest rates, sometimes to zero, and creates new money to buy bonds. That pushes up the price of stocks and houses. [dramatically] So the people who already own them are rescued TWICE. First by the bailout. Then by the new money.",
  "[confident] So let's answer the three questions. Where does money come from? Mostly from loans, typed into existence. Who gets it first? Those closest to the banks. [dramatically] And why does the same paycheck make one person rich... and keep another poor? [softly] Let's go back to our hundred-dollar bill."])),
 dict(beats=["B34", "B35", "B36", "B36b", "B36c", "B37"], text=P.join([
  "[warmly] The same bill. In Jake's hands, it's something to spend, or to park in an account that slowly eats it. [confident] In Ryan's hands, it's a tool. A tiny piece of things that grow while the dollar shrinks.",
  "[confident] That's the whole secret. Own things that grow when money is printed. Stay away from debt that charges you twenty percent. And don't let your long-term savings sit somewhere that pays less than inflation. [serious] This isn't financial advice. It's just how the game is played.",
  "[softly] Jake can't get those twenty years back. [warmly] But he finally knows the rules.",
  "[energetic] So Jake starts. Late, but he starts. He pays off the card first. Then five hundred dollars a month, automatically, into the same kind of fund Ryan chose. If the market does what it has done historically, and nothing is guaranteed, that could grow to over three hundred thousand dollars by the time Jake is sixty-five. [warmly] Not because he got smarter. Because he finally moved to the other side of the table.",
  "[warmly] Same salary. Same street. Different rules. [dramatically] Money was never the game... Knowing the rules is.",
  "[energetic] If this changed how you see money, subscribe. [mischievously] There's a lot more the banks will never tell you."])),
]
if __name__ == "__main__":
    print(sum(len(c["text"]) for c in CH), "Zeichen inkl. Tags")

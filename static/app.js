class BoggleGame{
    constructor(ID, seconds=60){ 
        this.seconds = seconds;
        this.makeTimer();
        this.score = 0;
        this.words = new Set();
        this.board = $('#' + ID);

        this.timer = setInterval(this.counter.bind(this), 1000);
        $('.submit_word', this.board).on('submit', this.submit.bind(this));
    }


    makeTimer(){
        $('.timer', this.board).text(this.seconds);
    }

    makeWord(word){
        $('.word_list', this.board).append($('<li>', {text: word}));
    }

    makeMessage(message, mClass){
        $('.message', this.board)
        .text(message)
        .removeClass()
        .addClass(`message ${mClass}`);
    }

    makeScore(){
        $('.score', this.board).text(this.score);
    }


    async submit(e){
        e.preventDefault();
        const $word = $('.word', this.board);

        let word = $word.val();

        if(!word) return;

        if(this.words.has(word)){
            this.makeMessage(`${word} has already been played`, 'error');
            return;
        }


        const res = await axios.get('/validate-word', {params: {word: word}});
        if(res.data.result === 'not-word'){
            this.makeMessage(`${word} is not an English word`, 'error');
        } else if( res.data.result === 'not-on-board'){
            this.makeMessage(`${word} is not on this game board`, 'error');
        } else {
            this.makeWord(word);
            this.score += word.length;
            this.makeScore();
            this.words.add(word);
            this.makeMessage(`Great word! Submitted: ${word}`, "good");
        }
        $word.val('').focus();
    }

    async counter(){
        this.seconds -= 1;
        this.makeTimer();

        if(this.seconds === 0){
            clearInterval(this.timer);
            await this.postScore();
        }
    }

    async postScore(){
        $('.submit_word', this.board).hide();
        const res = await axios.post('/post-score', { score: this.score });

        if(res.data.newHScore){
            this.makeMessage(`New high score: ${this.score}`, 'good');
        } else {
            this.makeMessage(`Final score: ${this.score}`, 'good');
        }
    }
}
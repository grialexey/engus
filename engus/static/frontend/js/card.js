var ONE_NUMBER_KEY_CODE = 49,
    TWO_NUMBER_KEY_CODE = 50,
    THREE_NUMBER_KEY_CODE = 51,
    FOUR_NUMBER_KEY_CODE = 52,
    FIVE_NUMBER_KEY_CODE = 53,
    SPACE_KEY_CODE = 32;

function Card($element) {
    this.init($element);
}

Card.prototype.init = function($element) {
    this.$el = $element;
    this.cacheElements();
    this.bindEvents();
};

Card.prototype.destroy = function() {
    this.unbindEvents();
    this.$el.remove();
};

Card.prototype.cacheElements = function() {
    this.$backOverlay = this.$el.find('.card__back-overlay');
    this.$backAudio = this.$el.find('.card__back-audio');
    this.$playBackAudioBtn = this.$el.find('.card__back-play-audio-btn');
    this.$confidence = this.$el.find('.card__confidence');
    this.$confidenceButtons = this.$el.find('.card__confidence-button');
};

Card.prototype.bindEvents = function() {
    this.$backOverlay.on('click', { self: this }, this.backOverlayClickEventHandler);
    this.$playBackAudioBtn.on('click', { self: this }, this.playBackAudioBtnClickEventHandler);
    $(document).on('keydown', { self: this }, this.documentKeyDownEventHandler);
    $(document).on('keyup', { self: this }, this.documentKeyUpEventHandler);
};

Card.prototype.unbindEvents = function() {
};

Card.prototype.backOverlayClickEventHandler = function(event) {
    var self = event.data.self;
    self.openAnswer();
};

Card.prototype.isAnswerOpened = function() {
    return this.$backOverlay.is('.m-active');
};

Card.prototype.openAnswer = function() {
    var self = this;
    this.$backOverlay.removeClass('m-active');
    this.playBackAudio();
    setTimeout(function() {
        self.openRatings();
    }, 0)
};

Card.prototype.playBackAudioBtnClickEventHandler = function(event) {
    var self = event.data.self;
    self.playBackAudio();
};

Card.prototype.documentKeyDownEventHandler = function(event) {
    var self = event.data.self;

    if (self.isAnswerOpened() && (event.which === SPACE_KEY_CODE)) {
        self.openAnswer();
    } else if (event.which === SPACE_KEY_CODE) {
        self.playBackAudio();
    }

    if (self.$confidence.is('.m-active')) {
        switch (event.which) {
            case ONE_NUMBER_KEY_CODE:
                self.$confidenceButtons.filter('[value=1]').addClass('m-active');
                break;
            case TWO_NUMBER_KEY_CODE:
                self.$confidenceButtons.filter('[value=2]').addClass('m-active');
                break;
            case THREE_NUMBER_KEY_CODE:
                self.$confidenceButtons.filter('[value=3]').addClass('m-active');
                break;
            case FOUR_NUMBER_KEY_CODE:
                self.$confidenceButtons.filter('[value=4]').addClass('m-active');
                break;
            case FIVE_NUMBER_KEY_CODE:
                self.$confidenceButtons.filter('[value=5]').addClass('m-active');
                break;
        }
    }
};

Card.prototype.documentKeyUpEventHandler = function(event) {
    var self = event.data.self;
    if (self.$confidence.is('.m-active')) {
        self.$confidenceButtons.removeClass('m-active');
        switch (event.which) {
            case ONE_NUMBER_KEY_CODE:
                self.$confidenceButtons.filter('[value=1]').trigger('click');
                break;
            case TWO_NUMBER_KEY_CODE:
                self.$confidenceButtons.filter('[value=2]').trigger('click');
                break;
            case THREE_NUMBER_KEY_CODE:
                self.$confidenceButtons.filter('[value=3]').trigger('click');
                break;
            case FOUR_NUMBER_KEY_CODE:
                self.$confidenceButtons.filter('[value=4]').trigger('click');
                break;
            case FIVE_NUMBER_KEY_CODE:
                self.$confidenceButtons.filter('[value=5]').trigger('click');
                break;
        }
    }
};

Card.prototype.playBackAudio = function() {
    if (this.$backAudio.length) {
        this.$backAudio[0].play();
    }
};

Card.prototype.openRatings = function() {
    this.$confidence.addClass('m-active');
    this.$confidence.fadeIn(250);
};
import React from 'react';

export default class InstaText extends React.Component {

    _renderText() {
        const words = this.props.text.split(' ');
        const wordsRendered = [];
        words.forEach((word, idx) => {
           if (word.startsWith('#')) {
               wordsRendered.push(<a className="insta-link" key={idx} target="_blank" href={InstaText.TAG_BASE_URL + word.slice(1)}>{word}</a>);
           } else if (word.startsWith('@')) {
               wordsRendered.push(<a className="insta-link" key={idx} target="_blank" href={InstaText.USER_BASE_URL + word.slice(1)}>{word}</a>);
           } else {
               wordsRendered.push(word)
           }
           wordsRendered.push(' ');
        });
        return wordsRendered;
    }

    render() {
        return (
            <span>
                {this._renderText()}
            </span>
        );
    }

}

InstaText.propTypes = {
    text: React.PropTypes.string
};

InstaText.defaultProps = {
    text: ''
};

InstaText.displayName = 'InstaText';

InstaText.TAG_BASE_URL = 'http://www.instagram.com/explore/tags/';
InstaText.USER_BASE_URL = 'http://www.instagram.com/';
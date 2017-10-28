import React from 'react';

export default class InstaUserLink extends React.Component {

    render() {
        return (
            <a target="_blank" className="insta-link user-link" href={'http://www.instagram.com/' + this.props.username +  '/'}>
                {this.props.username}
            </a>
        );
    }

}

InstaUserLink.propTypes = {
    username: React.PropTypes.string
};

InstaUserLink.defaultProps = {
    username: ''
};

InstaUserLink.displayName = 'InstaUserLink';
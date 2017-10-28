import React from 'react';
import InstaUserLink from "../../layout/InstaUserLink";

export default class UserCard extends React.Component {

    render() {
        return (
            <div className="user-card">
                <div className="item-img">
                    <img src={this.props.imgSrc}/>
                </div>
                <div className="username"><InstaUserLink username={this.props.userName}/></div>
                <div className="fullname">{this.props.fullName}</div>
            </div>
        );
    }

}

UserCard.propTypes = {
    userName: React.PropTypes.string,
    fullName: React.PropTypes.string,
    imgSrc: React.PropTypes.string
};

UserCard.defaultProps = {
    userName: '',
    fullName: '',
    imgSrc: null
};

UserCard.displayName = 'UserCard';
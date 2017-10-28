import React from 'react';
import ListView from "../../layout/ListView";
import TargetsListItem from "./TargetsListItem";
import ContentBox from "../../layout/ContentBox";

export default class TargetsList extends React.Component {

    render() {
        return (
            <ContentBox>
                <ListView loading={this.props.loading} emptyListText={'No users found. Add users to the list using the search bar.'}>
                {this.props.users.map((user, i) =>
                        <TargetsListItem
                        className="target-list-item"
                        key={i}
                        user={user}
                        onClick={(e) => this.props.onClick(e)} />
                        )}
                </ListView>
            </ContentBox>
        );
    }

}

TargetsList.propTypes = {
    users: React.PropTypes.arrayOf(React.PropTypes.object),
    onClick: React.PropTypes.func,
    loading: React.PropTypes.bool
};

TargetsList.defaultProps = {
    users: [],
    onClick: () => {},
    loading: false
};

TargetsList.displayName = 'TargetsList';
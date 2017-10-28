import React from 'react';
import ListView from "../../layout/ListView";
import FollowingsListItem from "./FollowingsListItem";
import SortFilterBar from "../../layout/SortFilterBar";
import ContentBox from "../../layout/ContentBox";

export default class FollowingsList extends React.Component {

    constructor(props) {
        super(props);
        this.state = {filterFunc: (items) => items};
    }

    _onVisibleItemsChanged(filterFunc) {
        this.setState({filterFunc: filterFunc});
    }

    render() {
        const visibleUsers = this.state.filterFunc(this.props.users);
        const itemsRendered = visibleUsers.map((user, i) =>
                        <FollowingsListItem
                        className="followings-list-item"
                        key={i}
                        user={user}
                        onClick={() => this.props.onClick(i)} />
                        );

        return (
            <ContentBox>
            <ListView emptyListText={'No followings found.'} loading={this.props.loading} sortFunc={FollowingsList.itemSortFunc} onItemFuncChanged={(items) => this._onVisibleItemsChanged(items)}>
                {itemsRendered}
            </ListView>
            </ContentBox>
        );
    }

}

FollowingsList.propTypes = {
    users: React.PropTypes.arrayOf(React.PropTypes.object),
    onClick: React.PropTypes.func,
    loading: React.PropTypes.bool
};

FollowingsList.defaultProps = {
    users: [],
    onClick: () => {},
    loading: false
};

FollowingsList.displayName = 'FollowingsList';

FollowingsList.itemSortFunc = (u0, u1) => {
    const cmp = u0.activity - u1.activity;
    if (cmp === 0) {
        return (u0.username.localeCompare(u1.username));
    } else {
        return cmp;
    }
};

FollowingsList.filters = [{
    name: 'inc',
    displayName: 'increasing only',
    filterFunc: (u) => u.activity >= 1
}];
/**
 * Created by PerArne on 17.07.2014.
 */


var sampleApp = angular.module('uiatimeplan', [
    'ngResource',
    'ngRoute',
    'ngCookies',
    'mobile-angular-ui'
]);
sampleApp.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
            when('/', {
                templateUrl: 'app/views/List.html',
                controller: 'ListController'
            }).
            when('/course/:course', {
                templateUrl: 'app/views/Course.html',
                controller: 'CourseController'
            }).
            when('/admin', {
                templateUrl: 'app/views/Admin.html',
                controller: 'AdminController'
            }).
            otherwise({
                redirectTo: '/'
            });
    }]);


///////////////////////////////////////
///
/// Resources
///
////////////////////////////////////////
sampleApp.factory('CourseListResource', function($resource) {
    return $resource('/course/list', {}, {
        'get': {method: 'GET', isArray: true}
    });
});

sampleApp.factory('CourseResource', function($resource) {
    return $resource('/course/item/:id', { id: '@id'}, {
        'get': {method: 'GET', isArray: false}
    });
});

sampleApp.factory('CourseInfoResource', function($resource) {
    return $resource('/course/info/:id', { id: '@id'}, {
        'get': {method: 'GET', isArray: false}
    });
});


sampleApp.factory('AdminUpdateResource', function($resource) {
    return $resource('/admin/update/:year/:semester', { year: '@year', semester: '@semester'}, {
        'post': {method: 'POST', isArray: false}
    });
});


sampleApp.filter('filterDay', function($filter){

    return function(items, subject) {

        filtered_items = [];

        var compare_date = new Date(Date.parse(subject));
        compare_date.setSeconds(0);
        compare_date.setMinutes(0);
        compare_date.setHours(0);
        compare_date.setMilliseconds(0);

        for(var idx in items) {
            var itm = items[idx];

            var dateTime = new Date(itm.date_from);
            dateTime.setSeconds(0);
            dateTime.setMinutes(0);
            dateTime.setHours(0);
            dateTime.setMilliseconds(0);


            //console.log(compare_date.getTime() + " - " + dateTime.getTime());
            if (compare_date.getTime() == dateTime.getTime())
                filtered_items.push(itm);
        }



        return filtered_items;
    };

});


sampleApp.controller("MainController", function($scope, $cookies){

    // Create array in cookie storage if not exist
    console.log($cookies.favourites)
    if(!$cookies.favourites) {
        $cookies.favourites = "";
    }


});



sampleApp.controller("MenuController", function($scope, CourseInfoResource, $cookies){

    var favourites = $cookies.favourites.split(";");
    $scope.courses = [];

    angular.forEach(favourites, function(value, key) {
        if(!!value) {
            $scope.courses.push(CourseInfoResource.get({id: value}));
        }
    });


});


sampleApp.controller("ListController", function($scope, CourseListResource){
    $scope.courses = CourseListResource.get();
    $scope.type = "studentsets";
    $scope.year = new Date().getFullYear();
    $scope.search = "";

    var  currentMonth = new Date().getMonth();



    var year = 2015;
    var range = [];
    range.push(year);
    for(var i=1;i<5;i++) {
        range.push(year + i);
    }
    $scope.years = range;
    $scope.semesters = [{
        id: 1,
        name: "Spring",
        value: "v"
    },
        {
            id: 2,
            name: "Autumn",
            value: "h"
        }];


    // Spring (Vår)
    if(currentMonth >= 0 && currentMonth <= 6)
        $scope.semester = $scope.semesters[0];
    else
        $scope.semester = $scope.semesters[1];





});

sampleApp.controller("AdminController", function($scope, AdminUpdateResource){

    var year = new Date().getFullYear();
    var range = [];
    range.push(year);
    for(var i=1;i<20;i++) {
        range.push(year + i);
    }
    $scope.years = range;


    $scope.update = function(){


        AdminUpdateResource.post({
            year: $scope.selected_year,
            semester: $scope.selected_semester
        })

    }


});



sampleApp.controller("CourseController", function($scope, $routeParams, $cookies, CourseResource ){
    var courseID = $routeParams.course;

    CourseResource.get({id : courseID}, function(result){
        $scope.course = result.course;
        $scope.courseItems = result.items;
        $scope.dates = result.dates;
    });




    var d = new Date();
    d.setHours(0,0,0,0);
    $scope.now = d.getTime();


    $scope.isFavourite = ($cookies.favourites.indexOf(courseID) > -1) ? true : false;

    $scope.addFavourite = function(){
        if(!($cookies.favourites.indexOf(courseID) > -1))
        {
            $cookies.favourites =   $cookies.favourites + ";" + courseID
            $scope.isFavourite = true;
            window.location.reload();
        }
    }

    $scope.removeFavourite = function(){
        if($cookies.favourites.indexOf(courseID) > -1)
        {
            $cookies.favourites =   $cookies.favourites.replace(";"+courseID, "");
            $scope.isFavourite = false;
            window.location.reload();
        }
    }



});

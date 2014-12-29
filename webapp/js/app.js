// Angular Module
PredictApp = angular.module("PredictApp", ['ngRoute']);
PredictApp.constant("API_END_POINT","http://apps.sampathweb.com/sentiment-analysis/api");

// Routes
PredictApp.config(function($routeProvider) {

    $routeProvider
    .when('/', {
        templateUrl: 'pages/main.html',
        controller: 'mainCtrl'
    })
    .when('/datasets', {
        templateUrl: 'pages/dataset.html',
        controller: 'datasetCtrl'
    })
    .otherwise({
         redirectTo: '/'
      });
});


// Services
PredictApp.service('predictSrv', ['$http', 'API_END_POINT', function($http, API_END_POINT) {

    var self = this;

    self.load_datasets = function(refresh) {
        var request = $http.jsonp(API_END_POINT + '/datasets/?callback=JSON_CALLBACK');
        return request.then(handleSuccess, handleError);
    };

    self.upload = function(new_ds) {
        var fd = new FormData();
        fd.append("name", new_ds.name);
        fd.append("file", new_ds.file);
        console.log(fd);

        return $http.post(API_END_POINT + '/datasets/new/', fd, {
            withCredentials: false,
            headers: {'Content-Type': undefined },
            transformRequest: angular.identity
        });
    };

    self.predict = function(dataset, new_text) {
        var pred_result = {};
        var pred_api;
        var params = {
            'callback': 'JSON_CALLBACK',
            'dataset': dataset.name,
            'text': new_text
        };

        var request = $http.jsonp(API_END_POINT + '/predictors/', {
            params: params
        });
        return request.then(handleSuccess, handleError);
    };

    // Transform the successful response, unwrapping the application data
    function handleError(response) {
        console.log(response);
        return(response.data);
    }
    // Transform the successful response, unwrapping the application data
    function handleSuccess(response) {
        return(response.data);
    }
}]);

// Controllers
PredictApp.controller('mainCtrl', ['$scope', 'predictSrv', function($scope, predictSrv) {

    // User Input of review
    $scope.selected_ds = '';
    $scope.new_review = '';
    // Results Table
    $scope.pred_results = [];

    predictSrv.load_datasets().then(function (data) {
        $scope.datasets = data.datasets;
    });

    $scope.submit = function() {
        console.log($scope.new_review);
        console.log($scope.selected_ds);
        predictSrv.predict($scope.selected_ds, $scope.new_review).then(function(data) {
            console.log(data);
            $scope.pred_results.push(data.predicted);
        });
    }
}]);

PredictApp.controller('datasetCtrl', ['$scope', 'predictSrv', function($scope, predictSrv) {

    $scope.refresh_data = function() {
        predictSrv.load_datasets().then(function (data) {
            $scope.datasets = data.datasets;
        });
    };

    $scope.initialize = function() {
        $scope.new_ds = {name: '', file: null};
        $scope.refresh_data();
    };

    $scope.upload = function() {
        predictSrv.upload($scope.new_ds).then($scope.initialize);

    };

    $scope.delete = function(ds) {
        console.log(ds);
    };

    $scope.setFiles = function(element) {
        $scope.new_ds.file = element.files[0];
    };

    // Run Initialize
    $scope.initialize();

}]);

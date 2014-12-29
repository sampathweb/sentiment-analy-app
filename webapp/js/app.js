// Angular Module
PredictApp = angular.module("PredictApp", ['ngRoute']);
// PredictApp.constant("API_END_POINT","http://apps.sampathweb.com/sentiment-analysis/api");
PredictApp.constant("API_END_POINT","http://127.0.0.1:5000");

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

    self.delete = function(ds) {
        var fd = new FormData();
        fd.append("name", ds.name);

        return $http.post(API_END_POINT + '/datasets/delete/', fd, {
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

    // Transform the successful and error responses
    function handleError(response) {
        console.log(response);
        return(response.data);
    }
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

    $scope.messages = [
        'Uploaded Files need to be less than 3MB.',
        'Files need to be with extension txt, csv or tsv',
        'Files need to be in Two Column Format with First Column containing the Target Category and Second Column with the Text'
    ];

    $scope.initialize = function() {
        $scope.new_ds = {name: '', file: null};
        $scope.refresh_data();
    };

    $scope.upload = function() {
        $scope.upload_messages = [];
        if ($scope.new_ds.name.length == 0) {
            alert('Dataset Name cannot be empty.  Please enter a dataset name and then click Add');
        } else {
            predictSrv.upload($scope.new_ds).then($scope.initialize);
        }
    };

    $scope.delete = function(ds) {
        predictSrv.delete(ds).then($scope.initialize);
    };

    $scope.setFiles = function(element) {
        $scope.new_ds.file = element.files[0];
    };

    // Run Initialize
    $scope.initialize();

}]);

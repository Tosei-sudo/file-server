window.onload = init();

// use angularJS
function init() {
    const app = angular.module('myApp', []);
    app.controller('MainController', function ($scope, $http) {
        vm = this;

        vm.title = 'Hello AngularJS';

        vm.submit = async function () {
            let fd = new FormData();
            let ele = $("#file_selector")[0];
            let file = ele.files[0];

            fd.append('file', file);

            let res = await $http.post('/api/upload', fd, {
                transformRequest: angular.identity,
                headers: { 'Content-Type': undefined }
            });
            let tmp_path = res.data.path_list[0];
            let file_name = "base/" + file.name;

            let data = {
                'from': tmp_path,
                'to': file_name
            };
            res = await $http({
                method: 'put',
                url: '/api/move',
                params: data
            });
            console.log(res.data);
        }
    });
}
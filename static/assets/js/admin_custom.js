
(function($) {
    $(document).ready(function() {
        // Function to toggle visibility of media fields
        function toggleMediaFields() {
            var mediaType = $('#id_media_type').val();
            if (mediaType === 'image') {
                $('.form-row.field-img').show();
                $('.form-row.field-video').hide();
            } else if (mediaType === 'video') {
                $('.form-row.field-img').hide();
                $('.form-row.field-video').show();
            }
        }

        // Initial toggle on page load
        toggleMediaFields();

        // Toggle when media_type changes
        $('#id_media_type').change(function() {
            toggleMediaFields();
        });
    });
})(django.jQuery);

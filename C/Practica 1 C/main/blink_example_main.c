#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "led_strip.h"
#include "sdkconfig.h"

static const char *TAG = "example";

#define BLINK_GPIO CONFIG_BLINK_GPIO

#ifdef CONFIG_BLINK_LED_STRIP

static led_strip_handle_t led_strip;

/* Tabla de colores para el barrido */
static const uint8_t colores[][3] = {
    {255,   0,   0},   // Rojo
    {255, 165,   0},   // Naranja
    {255, 255,   0},   // Amarillo
    {  0, 255,   0},   // Verde
    {  0,   0, 255},   // Azul
    {128,   0, 128},   // Morado
    {  0,   0,   0}    // Apagado
};

#define NUM_COLORES (sizeof(colores) / sizeof(colores[0]))

static void configure_led(void)
{
    ESP_LOGI(TAG, "Configurado para barrido de colores");

    /* Configuración del LED direccionable */
    led_strip_config_t strip_config = {
        .strip_gpio_num = BLINK_GPIO,
        .max_leds = 1,
    };

#if CONFIG_BLINK_LED_STRIP_BACKEND_RMT
    led_strip_rmt_config_t rmt_config = {
        .clk_src = RMT_CLK_SRC_DEFAULT,
        .mem_block_symbols = 64,
        .flags.with_dma = false,
    };

    ESP_ERROR_CHECK(
        led_strip_new_rmt_device(&strip_config, &rmt_config, &led_strip)
    );

#elif CONFIG_BLINK_LED_STRIP_BACKEND_SPI
    led_strip_spi_config_t spi_config = {
        .spi_bus = SPI2_HOST,
        .flags.with_dma = true,
    };

    ESP_ERROR_CHECK(
        led_strip_new_spi_device(&strip_config, &spi_config, &led_strip)
    );
#else
#error "unsupported LED strip backend"
#endif

    led_strip_clear(led_strip);
}

#elif CONFIG_BLINK_LED_GPIO
#error "Este código es solo para LED direccionable (NeoPixel)"
#else
#error "unsupported LED type"
#endif

void app_main(void)
{
    configure_led();

    int i = 0;

    while (1) {
        ESP_LOGI(TAG, "Color %d -> R:%d G:%d B:%d",
                 i,
                 colores[i][0],
                 colores[i][1],
                 colores[i][2]);

        led_strip_set_pixel(
            led_strip, 0,
            colores[i][0],
            colores[i][1],
            colores[i][2]
        );
        led_strip_refresh(led_strip);

        i = (i + 1) % NUM_COLORES;

        vTaskDelay(CONFIG_BLINK_PERIOD / portTICK_PERIOD_MS);
    }
}


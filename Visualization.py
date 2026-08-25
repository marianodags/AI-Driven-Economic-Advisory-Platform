import matplotlib.pyplot as plt

def plot_results(dates, y_actual, y_pred, test_indices, show=True, save_path=None):
    """
    Plots actual vs predicted GDP growth over time.
    """
    plt.figure()
    plt.plot(dates, y_actual, label='Actual GDP Growth')
    plt.plot(dates.iloc[test_indices], y_pred, 'o', label='Predicted GDP Growth')
    plt.legend()
    plt.title('Actual vs Predicted GDP Growth')
    plt.xlabel('Date')
    plt.ylabel('GDP Growth')
    if save_path:
        plt.savefig(save_path)
    if show:
        plt.show()
    plt.close()
